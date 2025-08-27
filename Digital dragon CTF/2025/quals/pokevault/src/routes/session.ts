import { Router, Request, Response } from "express";
import { readFileSync } from "fs";
import { join } from "path";
import { requireActiveSession } from "../middleware/auth";
import { SessionManager, VaultLockHelper } from "../services";

const router = Router();

const handleError = (res: Response, error: any): void => {
	res.status(500).json({
		success: false,
		error: error.message,
	});
};

router.post("/start", (req: Request, res: Response) => {
	try {
		const session = SessionManager.startSession();
		res.json({
			success: true,
			data: {
				sessionId: session.id,
				expiresAt: session.expiresAt,
				timeRemaining: SessionManager.getTimeRemaining(session),
				publicKey: session.vaultLock.publicKey.toString("hex"),
				vaults: session.vaultLock.vaults,
				selectedPokemon: session.vaultLock.selectedPokemon,
			},
			message: "Session started",
		});
	} catch (error: any) {
		handleError(res, error);
	}
});

router.get("/status/:sessionId", (req: Request, res: Response) => {
	try {
		const { sessionId } = req.params;

		if (!sessionId) {
			return res.status(400).json({
				success: false,
				error: "Session ID is required",
			});
		}

		const activeSession = SessionManager.getSession(sessionId);
		res.json({
			success: true,
			data: {
				hasActiveSession: !!activeSession,
				sessionId: activeSession?.id,
				expiresAt: activeSession?.expiresAt,
				publicKey: activeSession?.vaultLock.publicKey.toString("hex"),
				vaults: activeSession?.vaultLock.vaults,
				selectedPokemon: activeSession?.vaultLock.selectedPokemon,
				timeRemaining: activeSession
					? SessionManager.getTimeRemaining(activeSession)
					: undefined,
			},
		});
	} catch (error: any) {
		handleError(res, error);
	}
});

router.delete("/:sessionId", (req: Request, res: Response) => {
	try {
		const { sessionId } = req.params;
		const success = SessionManager.endSession(sessionId);
		res.json({
			success,
			message: success ? "Session ended" : "Session not found",
		});
	} catch (error: any) {
		handleError(res, error);
	}
});

router.post("/verify", requireActiveSession, (req: Request, res: Response) => {
	try {
		const { password } = req.body;
		const sessionId = (req as any).sessionId;
		const userSession = (req as any).userSession;

		if (!password) {
			return res.status(400).json({
				success: false,
				error: "Password is required",
			});
		}

		const result = VaultLockHelper.verify(password, userSession);

		if (!result.success) {
			userSession.failures = (userSession.failures || 0) + 1;
			if (userSession.failures >= 5) {
				SessionManager.endSession(sessionId);
				return res.status(403).json({
					success: false,
					error: "Maximum number of failures reached. Session ended.",
				});
			}
			return res.status(400).json({
				success: false,
				error: result.error + ` (Failures: ${userSession.failures}/5)`,
			});
		}

		const flag = process.env.FLAG || "DDC{FAKE_FLAG_FAKE_FLAG}";
		res.json({
			success: true,
			message: `Challenge completed: ${flag}`,
		});
	} catch (error: any) {
		handleError(res, error);
	}
});

router.get("/pokedex", (req: Request, res: Response) => {
	try {
		const pokedexPath = join(__dirname, "../data/pokedex.json");
		const pokedexData = JSON.parse(readFileSync(pokedexPath, "utf8"));
		res.json({
			success: true,
			data: pokedexData,
		});
	} catch (error: any) {
		res.status(500).json({
			success: false,
			error: "Failed to load Pokedex data",
		});
	}
});

export default router;
