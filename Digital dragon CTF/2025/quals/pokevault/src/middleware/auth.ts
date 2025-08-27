import { Request, Response, NextFunction } from "express";
import { SessionManager } from "../services";

export function requireActiveSession(
	req: Request,
	res: Response,
	next: NextFunction,
) {
	const sessionId = req.headers.authorization?.replace("Bearer ", "");

	if (!sessionId) {
		return res.status(400).json({
			success: false,
			error: "Session token is required in Authorization header",
		});
	}

	const activeSession = SessionManager.getSession(sessionId);
	if (!activeSession) {
		return res.status(401).json({
			success: false,
			error: "Invalid or expired session. Please start a new session.",
		});
	}

	(req as any).userSession = activeSession;
	(req as any).sessionId = sessionId;
	next();
}
