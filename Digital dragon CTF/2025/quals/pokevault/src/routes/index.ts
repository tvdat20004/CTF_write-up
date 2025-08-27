import { Router } from "express";
import sessionRouter from "./session";

const router = Router();

router.use("/session", sessionRouter);

export default router;
