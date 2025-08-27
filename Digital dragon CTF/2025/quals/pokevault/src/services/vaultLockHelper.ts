import { Pokemon, VaultLock as VaultLockType } from "../types";
import * as secp256k1 from "secp256k1";
import { createHash, randomUUID } from "crypto";
import { readFileSync } from "fs";
import { join } from "path";

export class VaultLockHelper {
	private static pokedexData: Pokemon[] = [];

	static async initialize() {
		try {
			const data = JSON.parse(
				readFileSync(join(__dirname, "../data/pokedex.json"), "utf8"),
			);
			this.pokedexData = data;
		} catch (error) {
			console.error("Failed to load Pokedex data:", error);
			this.pokedexData = [];
		}
	}

	private static getRandomPokemon(): Pokemon[] {
		if (this.pokedexData.length < 12) {
			throw new Error("Insufficient Pokemon data");
		}

		const shuffled = [...this.pokedexData].sort(() => Math.random() - 0.5);
		return shuffled.slice(0, 12);
	}

	private static generateBuffer(pokemonIds: number[]): Buffer {
		const buffer = Buffer.alloc(32);
		for (let i = 0; i < 12; i++) {
			buffer.writeUInt16LE(pokemonIds[i], i * 2);
		}
		buffer.reverse();
		return buffer;
	}

	private static generatePrivateKey(pokemonIds: number[]): Buffer {
		return createHash("sha256").update(Buffer.from(pokemonIds)).digest();
	}

	private static shufflePokemonIds(pokemonIds: number[]): number[] {
		const shuffled = [...pokemonIds];
		let i = shuffled.length - 1;
		while (i > 0) {
			i--;
			const j = Math.floor(Math.random() * (i + 1));
			[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
		}
		return shuffled;
	}

	static generateVaultLock(): VaultLockType {
		if (!this.pokedexData.length) throw new Error("Data not initialized");

		const selectedPokemon = this.getRandomPokemon();

		const pokemonIds = selectedPokemon.map((p) => p.id);
		const privateKey = this.generatePrivateKey(pokemonIds);
		
		const publicKey = Buffer.from(secp256k1.publicKeyCreate(privateKey));
		console.log("Private Key:", privateKey.toString("hex"));
		const vaults = Array.from({ length: 6 }, () => {
			const vaultId = randomUUID();
			const shuffledIds = this.shufflePokemonIds(pokemonIds);

			const nonce = this.generateBuffer(shuffledIds);
			console.log(nonce.toString("hex"));
			// console.log(nonce);
			
			const messageHash = createHash("sha256").update(vaultId).digest();
			const signature = secp256k1.ecdsaSign(messageHash, privateKey, {
				noncefn: () => nonce,
			});

			return {
				id: vaultId,
				signature: Buffer.from(signature.signature).toString("hex"),
			};
		});

		return {
			privateKey,
			publicKey,
			vaults,
			selectedPokemon: selectedPokemon.sort((a, b) => a.id - b.id),
		} as VaultLockType;
	}

	static verify(
		password: string,
		session: { vaultLock: VaultLockType },
	): {
		success: boolean;
		content?: string;
		error?: string;
	} {
		if (!session) {
			return { success: false, error: "Session not found" };
		}

		const pokemonNames = password
			.split(/[,\s]+/)
			.map((name) => name.trim())
			.filter((n) => n.length > 0);

		if (pokemonNames.length !== 12) {
			return {
				success: false,
				error: "Password must contain exactly 12 Pokémon names",
			};
		}
		const selectedPokemon = session.vaultLock.selectedPokemon;
		const pokemonNameToId = new Map();
		selectedPokemon.forEach((p) => pokemonNameToId.set(p.name, p.id));

		const pokemonIds = [];
		for (const name of pokemonNames) {
			const id = pokemonNameToId.get(name);
			if (id === undefined) {
				return { success: false, error: `Unknown Pokémon: ${name}` };
			}
			pokemonIds.push(id);
		}
		const privateKey = this.generatePrivateKey(pokemonIds);
		const expectedPrivateKey = session.vaultLock.privateKey;

		if (Buffer.compare(privateKey, expectedPrivateKey) !== 0) {
			return {
				success: false,
				error: "Invalid password",
			};
		}

		return {
			success: true,
			content: "Vault unlocked successfully!",
		};
	}
}
