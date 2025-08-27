import express, {
	Request,
	Response,
	NextFunction,
	ErrorRequestHandler,
} from "express";
import cors from "cors";
import path from "path";
import { Server } from "http";
import apiRoutes from "./routes";
import { VaultLockHelper } from "./services";

const app = express();
const PORT = Number(process.env.PORT) || 25001;
const HOST = "0.0.0.0";

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, "..", "public")));

app.use("/api", apiRoutes);

app.get("/", (req, res) =>
	res.render("index", { title: "PokeVault", description: "" }),
);

app.use((req, res) =>
	res.status(404).render("404", { title: "404 - Page Not Found" }),
);

async function initializeApp() {
	try {
		await VaultLockHelper.initialize();
		console.log("Pokemon data initialized successfully");
	} catch (error) {
		console.error("Failed to initialize Pokemon data:", error);
	}
}

app.use(((error: any, req: Request, res: Response, next: NextFunction) => {
	console.error("Server error:", error);
	res.status(500).json({ success: false, error: "Internal server error" });
}) as ErrorRequestHandler);

let server: Server;

initializeApp()
	.then(() => {
		server = app.listen(PORT, HOST, () => {
			console.log(`PokeVault Platform running on http://${HOST}:${PORT}`);
		});

		server.on("error", (error) => console.error("Server error:", error));

		const gracefulShutdown = () => {
			console.log("Shutting down gracefully");
			server.close(() => process.exit(0));
		};

		process.on("SIGINT", gracefulShutdown);
		process.on("SIGTERM", gracefulShutdown);
	})
	.catch((error) => {
		console.error(
			"Failed to initialize Pokemon data. Server not started.",
			error,
		);
		process.exit(1);
	});

process.on("uncaughtException", (error) => {
	console.error("Uncaught Exception:", error);
	process.exit(1);
});

process.on("unhandledRejection", (reason, promise) => {
	console.error("Unhandled Rejection at:", promise, "reason:", reason);
	process.exit(1);
});

export default app;
