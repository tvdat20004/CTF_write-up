import { UserSession, VaultLock } from "../types";
import { VaultLockHelper } from "./vaultLockHelper";
import { randomUUID } from "crypto";

export class SessionManager {
	private static sessions: Map<string, UserSession> = new Map();
	private static readonly SESSION_DURATION_MS = 5 * 60 * 1000;

	static generateSessionId(): string {
		return randomUUID();
	}

	static startSession(): UserSession {
		const sessionId = this.generateSessionId();
		const startTime = new Date();
		const expiresAt = new Date(
			startTime.getTime() + this.SESSION_DURATION_MS,
		);
		const vaultLock: VaultLock = VaultLockHelper.generateVaultLock();

		const session: UserSession = {
			id: sessionId,
			startTime,
			expiresAt,
			isActive: true,
			vaultLock,
			failures: 0,
		};

		this.sessions.set(sessionId, session);
		return session;
	}

	static getSession(sessionId: string): UserSession | null {
		const session = this.sessions.get(sessionId);
		if (!session) return null;

		if (!this.isSessionValid(session)) {
			this.endSession(sessionId);
			return null;
		}

		return session;
	}

	static isSessionValid(session: UserSession): boolean {
		return session.isActive && new Date() < session.expiresAt;
	}

	static endSession(sessionId: string): boolean {
		const session = this.sessions.get(sessionId);
		if (!session) return false;
		session.isActive = false;
		this.sessions.delete(sessionId);
		return true;
	}

	static getTimeRemaining(session: UserSession): number {
		return this.isSessionValid(session)
			? Math.max(0, session.expiresAt.getTime() - Date.now())
			: 0;
	}

	static cleanupExpiredSessions(): void {
		const now = new Date();
		for (const [sessionId, session] of this.sessions.entries()) {
			if (now >= session.expiresAt) {
				this.endSession(sessionId);
			}
		}
	}
}

setInterval(() => SessionManager.cleanupExpiredSessions(), 5 * 60 * 1000);
