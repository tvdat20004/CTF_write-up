export interface VaultLock {
	privateKey: Buffer;
	publicKey: Buffer;
	vaults: Array<{
		id: string;
		signature: string;
	}>;
	selectedPokemon: Array<{
		id: number;
		name: string;
	}>;
}

export interface Pokemon {
	id: number;
	name: string;
}

export interface UserSession {
	id: string;
	startTime: Date;
	expiresAt: Date;
	isActive: boolean;
	vaultLock: VaultLock;
	failures: number;
}
