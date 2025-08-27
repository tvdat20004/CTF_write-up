let currentSessionToken = localStorage.getItem("sessionToken");
let currentSession = null;
let sessionTimer = null;
let currentPublicKey = null;
function showMessage(message, type = "error") {
	const messageDiv = document.getElementById("message");
	const messageElement = document.createElement("div");
	messageElement.className = `message ${type}`;
	messageElement.innerHTML = message;
	messageDiv.innerHTML = "";
	messageDiv.appendChild(messageElement);
	setTimeout(() => (messageDiv.innerHTML = ""), 3000);
}

async function checkSessionStatus() {
	if (!currentSessionToken) {
		currentSession = null;
		updateSessionUI(false);
		return;
	}
	try {
		const response = await fetch(
			`/api/session/status/${currentSessionToken}`,
		);
		const data = await response.json();
		if (data.success && data.data.hasActiveSession) {
			currentSession = {
				id: data.data.sessionId,
				expiresAt: data.data.expiresAt,
			};
			updateSessionUI(true, data.data.timeRemaining);
			startSessionTimer(data.data.timeRemaining);
			if (data.data.publicKey) {
				currentPublicKey = data.data.publicKey;
				showVaultInterface(data.data);
			}
		} else {
			clearSession();
		}
	} catch (error) {
		console.error("Error checking session status:", error);
		clearSession();
	}
}

async function startSession() {
	try {
		const response = await fetch("/api/session/start", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({}),
		});
		const data = await response.json();
		if (data.success) {
			currentSessionToken = data.data.sessionId;
			localStorage.setItem("sessionToken", currentSessionToken);
			currentSession = {
				id: data.data.sessionId,
				expiresAt: data.data.expiresAt,
			};
			updateSessionUI(true, data.data.timeRemaining);
			startSessionTimer(data.data.timeRemaining);
			if (data.data.publicKey) {
				currentPublicKey = data.data.publicKey;
				showVaultInterface(data.data);
			}
		} else {
			showMessage(data.error || "Failed to start session", "error");
		}
	} catch (error) {
		console.error("Error starting session:", error);
		showMessage("Network error. Please try again.", "error");
	}
}

async function endSession() {
	if (!currentSession) return;
	try {
		const response = await fetch(`/api/session/${currentSession.id}`, {
			method: "DELETE",
		});
		const data = await response.json();
		if (data.success) {
		}
	} catch (error) {
		console.error("Error ending session:", error);
	} finally {
		clearSession();
		if (sessionTimer) {
			clearInterval(sessionTimer);
			sessionTimer = null;
		}
		closeVaultSection();
	}
}

function startSessionTimer(timeRemaining) {
	if (sessionTimer) {
		clearInterval(sessionTimer);
	}
	let remaining = timeRemaining;
	sessionTimer = setInterval(() => {
		remaining -= 1000;
		if (remaining <= 0) {
			clearInterval(sessionTimer);
			sessionTimer = null;
			clearSession();
			closeVaultSection();
			showMessage(
				"<i class='fas fa-clock'></i> Training session expired! Please start a new session to continue.",
				"error",
			);
		} else {
			updateSessionTimer(remaining);
		}
	}, 1000);
}

function updateSessionTimer(timeRemaining) {
	const navTimer = document.getElementById("navTimer");
	if (!navTimer) return;
	const minutes = Math.floor(timeRemaining / 60000);
	const seconds = Math.floor((timeRemaining % 60000) / 1000);
	navTimer.textContent = `⏱️ ${minutes}:${seconds.toString().padStart(2, "0")}`;
}

function updateSessionUI(hasSession, timeRemaining = 0) {
	const sessionToggle = document.getElementById("sessionToggle");
	const navTimer = document.getElementById("navTimer");
	const publicKeyBtn = document.getElementById("publicKeyBtn");
	if (sessionToggle) {
		if (hasSession) {
			sessionToggle.textContent = "End Session";
			sessionToggle.onclick = endSession;
			sessionToggle.classList.add("active");
			if (navTimer) {
				navTimer.style.display = "inline";
				updateSessionTimer(timeRemaining);
			}
			if (publicKeyBtn) {
				publicKeyBtn.style.display = "flex";
			}
		} else {
			sessionToggle.textContent = "Start Session";
			sessionToggle.onclick = startSession;
			sessionToggle.classList.remove("active");
			if (navTimer) {
				navTimer.style.display = "none";
			}
			if (publicKeyBtn) {
				publicKeyBtn.style.display = "none";
			}
		}
	}
}

function showVaultInterface(data) {
	const vaultList = document.getElementById("vaultList");

	const vaults = data.vaults || [];
	let vaultsHTML = "";

	if (vaults.length > 0) {
		vaultsHTML = vaults
			.map(
				(vault, index) => `
			<div class="vault-card" data-vault-id="${vault.id}">
				<div class="vault-card-header" style="display: flex; justify-content: space-between; align-items: center;">
					<i class="fas fa-vault" style="color: var(--accent-primary);"></i>
					<button class="vault-open-btn btn btn-outline" onclick="openVaultModal('${vault.id}', '${vault.id}', '${data.sessionId}', '${data.publicKey}')" style="padding: 0.5rem 1rem; font-size: 0.85rem; margin: 0;">
						Open
					</button>
				</div>
				<div class="vault-info">
					<div class="vault-info-label">Vault ID</div>
					<div class="vault-info-value">${vault.id}</div>
				</div>
				<div class="vault-info" style="margin-bottom: 0;">
					<div class="vault-info-label">Signature</div>
					<div class="vault-info-value">${vault.signature}</div>
				</div>
			</div>
		`,
			)
			.join("");
	}

	vaultList.innerHTML = vaultsHTML;
	vaultList.style.display = "grid";
	vaultList.scrollIntoView({ behavior: "smooth" });

	window.currentSessionData = data;
}

function closeVaultSection() {
	const vaultList = document.getElementById("vaultList");
	if (vaultList) {
		vaultList.style.display = "none";
	}
}

function visualizePokemonGraph(graph, containerId, passwordInputId) {
	const container = document.getElementById(containerId);
	if (!container) {
		console.error("Container not found:", containerId);
		return;
	}

	if (!graph || !graph.vertices || !graph.edges) {
		console.error("Invalid graph data:", graph);
		return;
	}

	const containerElement = container.parentElement;
	const containerWidth = containerElement
		? containerElement.offsetWidth
		: window.innerWidth - 40;
	const screenWidth = window.innerWidth;

	let width, height;

	if (screenWidth <= 768) {
		width = Math.max(300, Math.min(screenWidth - 20, containerWidth - 20));
		height = Math.max(400, width * 0.8);
	} else if (screenWidth <= 1024) {
		width = Math.max(600, Math.min(800, containerWidth - 40));
		height = Math.max(450, width * 0.75);
	} else {
		width = Math.min(1200, Math.max(800, containerWidth - 40));
		height = Math.min(700, Math.max(500, width * 0.7));
	}

	if (width <= 0 || height <= 0) {
		console.warn("Invalid graph dimensions, using fallback");
		width = screenWidth <= 768 ? 350 : 1000;
		height = screenWidth <= 768 ? 400 : 600;
	}

	container.innerHTML = "";

	const svg = d3
		.select(`#${containerId}`)
		.append("svg")
		.attr("width", width)
		.attr("height", height);

	let circleRadius, imageSize, margin;

	if (screenWidth <= 768) {
		circleRadius = Math.max(14, Math.min(20, width / 25));
		margin = Math.max(30, circleRadius * 1.8);
	} else if (screenWidth <= 1024) {
		circleRadius = Math.max(18, Math.min(24, width / 35));
		margin = Math.max(40, circleRadius * 2);
	} else {
		circleRadius = Math.max(20, Math.min(28, width / 40));
		margin = Math.max(50, circleRadius * 2);
	}

	imageSize = circleRadius * 1.4;
	const imageOffset = -imageSize / 2;

	let pokemonNames;
	if (
		graph.vertices &&
		Array.isArray(graph.vertices) &&
		typeof graph.vertices[0] === "string"
	) {
		pokemonNames = new Set(graph.vertices);
	} else {
		pokemonNames = new Set();
		graph.edges.forEach(([name1, name2]) => {
			if (typeof name1 === "string") pokemonNames.add(name1);
			if (typeof name2 === "string") pokemonNames.add(name2);
		});
	}

	const nodes = Array.from(pokemonNames).map((name, i) => ({
		id: i,
		name: name,
		x: Math.random() * (width - 2 * margin) + margin,
		y: Math.random() * (height - 2 * margin) + margin,
	}));

	const nameToIndex = new Map();
	nodes.forEach((node, index) => {
		nameToIndex.set(node.name, index);
	});

	const edges = graph.edges
		? graph.edges
				.map(([pokemonA, pokemonB]) => {
					const sourceIndex = nameToIndex.get(pokemonA);
					const targetIndex = nameToIndex.get(pokemonB);

					return {
						source: nodes[sourceIndex],
						target: nodes[targetIndex],
					};
				})
				.filter((edge) => edge.source && edge.target)
		: []; // No edges for ECDSA mode

	let linkDistance, chargeStrength, collisionRadius;

	if (screenWidth <= 768) {
		linkDistance = Math.max(30, Math.min(50, width / 12));
		chargeStrength = Math.max(-200, Math.min(-100, -width * 0.3));
		collisionRadius = Math.max(15, Math.min(25, circleRadius * 1.2));
	} else if (screenWidth <= 1024) {
		linkDistance = Math.max(40, Math.min(70, width / 15));
		chargeStrength = Math.max(-300, Math.min(-150, -width * 0.4));
		collisionRadius = Math.max(20, Math.min(35, circleRadius * 1.3));
	} else {
		linkDistance = Math.max(50, Math.min(90, width / 18));
		chargeStrength = Math.max(-400, Math.min(-200, -width * 0.5));
		collisionRadius = Math.max(25, Math.min(40, circleRadius * 1.4));
	}

	const simulation = d3
		.forceSimulation(nodes)
		.force("link", d3.forceLink(edges).distance(linkDistance))
		.force("charge", d3.forceManyBody().strength(chargeStrength))
		.force("center", d3.forceCenter(width / 2, height / 2))
		.force("collision", d3.forceCollide().radius(collisionRadius))
		.force(
			"boundary",
			d3
				.forceX()
				.strength(0.05)
				.x(width / 2),
		)
		.force(
			"boundary-y",
			d3
				.forceY()
				.strength(0.05)
				.y(height / 2),
		);

	function dragstarted(event, d) {
		if (!event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	function dragged(event, d) {
		d.fx = event.x;
		d.fy = event.y;
	}

	function dragended(event, d) {
		if (!event.active) simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
	}

	const strokeWidth = Math.max(1, Math.min(2, width / 600));

	const link = svg
		.selectAll(".link")
		.data(edges)
		.enter()
		.append("line")
		.attr("class", "link")
		.style("stroke", "#999")
		.style("stroke-width", strokeWidth);

	const node = svg
		.selectAll(".node")
		.data(nodes)
		.enter()
		.append("g")
		.attr("class", "node")
		.call(
			d3
				.drag()
				.on("start", dragstarted)
				.on("drag", dragged)
				.on("end", dragended),
		);

	node.append("circle")
		.attr("r", circleRadius)
		.style("fill", "#ffffff")
		.style("stroke", "#ffcc02")
		.style("stroke-width", 3)
		.style("filter", "drop-shadow(0px 2px 4px rgba(0,0,0,0.2))");

	node.append("image")
		.attr("width", imageSize)
		.attr("height", imageSize)
		.attr("x", imageOffset)
		.attr("y", imageOffset)
		.attr("href", (d) => {
			return `/img/pokedex/${d.name.toLowerCase()}.png`;
		})
		.style("cursor", "pointer")
		.style("transition", "all 0.2s ease")
		.on("mouseover", function (event, d) {
			const hoverImageSize = imageSize * 1.15;
			const hoverImageOffset = -hoverImageSize / 2;
			const hoverCircleRadius = circleRadius * 1.15;

			d3.select(this)
				.transition()
				.duration(200)
				.attr("width", hoverImageSize)
				.attr("height", hoverImageSize)
				.attr("x", hoverImageOffset)
				.attr("y", hoverImageOffset);

			d3.select(this.parentNode)
				.select("circle")
				.transition()
				.duration(200)
				.attr("r", hoverCircleRadius)
				.style("stroke", "#ff6b6b")
				.style("stroke-width", 4);
		})
		.on("mouseout", function (event, d) {
			d3.select(this)
				.transition()
				.duration(200)
				.attr("width", imageSize)
				.attr("height", imageSize)
				.attr("x", imageOffset)
				.attr("y", imageOffset);

			d3.select(this.parentNode)
				.select("circle")
				.transition()
				.duration(200)
				.attr("r", circleRadius)
				.style("stroke", "#ffcc02")
				.style("stroke-width", 3);
		})
		.on("click", function (event, d) {
			const passwordInput = passwordInputId
				? document.getElementById(passwordInputId)
				: document.querySelector('textarea[id^="password-input-"]');
			if (passwordInput) {
				const currentValue = passwordInput.value.trim();

				const nodeElement = d3.select(this.parentNode);
				const isAlreadyClicked = nodeElement.classed("clicked");

				if (isAlreadyClicked) {
					return;
				}

				if (currentValue === "") {
					passwordInput.value = d.name;
				} else {
					passwordInput.value = currentValue + " " + d.name;
				}

				nodeElement.classed("clicked", true);

				nodeElement.transition().duration(300).style("opacity", 0.3);

				d3.select(this).style("cursor", "not-allowed");
			}
		})
		.on("error", function () {
			d3.select(this.parentNode)
				.append("text")
				.attr("text-anchor", "middle")
				.attr("dy", 4)
				.style("fill", "#2c3e50")
				.style("font-weight", "bold")
				.style("font-size", "8px")
				.text((d) =>
					d.name.length > 6 ? d.name.substring(0, 4) + "..." : d.name,
				);
		});

	let nameFontSize, nameOffset;

	if (screenWidth <= 768) {
		nameFontSize = Math.max(6, Math.min(8, width / 80));
		nameOffset = circleRadius + 8;
	} else if (screenWidth <= 1024) {
		nameFontSize = Math.max(7, Math.min(9, width / 100));
		nameOffset = circleRadius + 10;
	} else {
		nameFontSize = Math.max(7, Math.min(10, width / 120));
		nameOffset = circleRadius + 12;
	}

	node.append("text")
		.attr("text-anchor", "middle")
		.attr("dy", nameOffset)
		.style("fill", "#2c3e50")
		.style("font-weight", "bold")
		.style("font-size", `${nameFontSize}px`)
		.style("background", "rgba(255,255,255,0.8)")
		.text((d) => d.name);

	simulation.on("tick", () => {
		nodes.forEach((d) => {
			const padding = Math.max(35, circleRadius * 1.5);
			d.x = Math.max(padding, Math.min(width - padding, d.x));
			d.y = Math.max(padding, Math.min(height - padding, d.y));
		});

		link.attr("x1", (d) => d.source.x)
			.attr("y1", (d) => d.source.y)
			.attr("x2", (d) => d.target.x)
			.attr("y2", (d) => d.target.y);

		node.attr("transform", (d) => `translate(${d.x},${d.y})`);
	});
}

function initializeApp() {
	checkSessionStatus();
}

function clearSession() {
	currentSession = null;
	currentSessionToken = null;
	currentPublicKey = null;
	localStorage.removeItem("sessionToken");
	updateSessionUI(false);
}

let pokedexData = [];
let pokedexLoaded = false;

async function loadPokedexData() {
	if (pokedexLoaded) return;
	try {
		const response = await fetch("/api/session/pokedex");
		const data = await response.json();
		pokedexData = data.success ? data.data : [];
		pokedexLoaded = true;
	} catch (error) {
		console.error("Error loading Pokedex data:", error);
		pokedexData = [];
	}
}

function openPokedex() {
	const modal = document.getElementById("pokedexModal");
	modal.style.display = "block";
	displayPokemon();
}

function closePokedex() {
	const modal = document.getElementById("pokedexModal");
	modal.style.display = "none";
}

function showPublicKey() {
	if (!currentPublicKey) {
		alert("No public key available. Please start a session first.");
		return;
	}

	const modal = document.createElement("div");
	modal.className = "modal";
	modal.style.display = "block";
	modal.innerHTML = `
		<div class="modal-content" style="max-width: 600px;">
			<div class="modal-header">
				<h2><img src="/img/key.png" alt="Key" width="24" height="24" style="margin-right: 8px; vertical-align: middle;"> Public Key</h2>
				<span class="close" onclick="this.closest('.modal').remove()">&times;</span>
			</div>
			<div class="modal-body">
				<div>
					<div style="font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--text-primary); word-break: break-all; background: rgba(79, 134, 200, 0.05); padding: 1rem; border-radius: 8px; border: 1px solid rgba(79, 134, 200, 0.1); max-height: 200px; overflow-y: auto;">
						${currentPublicKey}
					</div>
				</div>
			</div>
		</div>
	`;

	document.body.appendChild(modal);

	modal.onclick = function (event) {
		if (event.target === modal) {
			modal.remove();
		}
	};
}

function displayPokemon() {
	const grid = document.getElementById("pokemonGrid");
	if (!pokedexData.length) {
		grid.innerHTML = "<p>Loading Pokémon data...</p>";
		return;
	}
	const fragment = document.createDocumentFragment();
	pokedexData.forEach((pokemon) => {
		const card = document.createElement("div");
		card.className = "pokemon-card";
		card.innerHTML = `
			<div class="pokemon-image">
				<img src="/img/pokedex/${pokemon.name.toLowerCase()}.png" alt="${pokemon.name}" onerror="this.style.display='none'">
			</div>
			<div class="pokemon-name">${pokemon.name}</div>
			<div class="pokemon-id">#${(pokemon.id + 252).toString().padStart(3, "0")}</div>`;
		fragment.appendChild(card);
	});
	grid.innerHTML = "";
	grid.appendChild(fragment);
}

window.onclick = function (event) {
	const modal = document.getElementById("pokedexModal");
	if (event.target === modal) {
		closePokedex();
	}
};

function openVaultModal(vaultId, vaultTitle, sessionId, publicKey) {
	const modal = document.getElementById("vaultModal");
	const modalTitle = document.getElementById("vaultModalTitle");
	const modalContent = document.getElementById("vaultModalContent");

	modalTitle.textContent = `Vault ${vaultId}`;

	const sessionData = window.currentSessionData;
	const selectedPokemon = sessionData ? sessionData.selectedPokemon : [];

	let pokemonHTML = "";
	if (selectedPokemon.length > 0) {
		pokemonHTML = selectedPokemon
			.map(
				(pokemon) => `
			<div class="pokemon-item" style="display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem; background: rgba(149, 226, 141, 0.05); border-radius: 8px; border: 1px solid rgba(149, 226, 141, 0.1);">
				<img src="/img/pokedex/${pokemon.name.toLowerCase()}.png" alt="${pokemon.name}" style="width: 32px; height: 32px;" onerror="this.style.display='none'">
				<span style="font-weight: 500; color: var(--text-primary);">${pokemon.name}</span>
			</div>
		`,
			)
			.join("");
	}

	modalContent.innerHTML = `
		<div style="max-width: 1200px; margin: 0 auto;">
			<div style="display: flex; gap: 2rem; align-items: center;">
				<div class="graph-container" style="flex: 7; padding: 1.5rem; background: rgba(79, 134, 200, 0.05); border-radius: 12px; border: 1px solid rgba(79, 134, 200, 0.1);">
					<h4 style="margin-bottom: 1rem; color: var(--text-primary); font-size: 1.1rem; font-weight: 600;">
						<i class='fas fa-fingerprint'></i> Vault Helper
					</h4>
					<div id="modal-graph-viz-${vaultId}" class="graph-viz" style="margin: 0 auto;"></div>
				</div>
				<div class="password-input" style="flex: 3;">
					<h4 style="margin-bottom: 0.75rem; color: var(--text-primary); font-size: 1.1rem; font-weight: 600;">
						<i class='fas fa-lock'></i> Enter Vault Password
					</h4>
					<textarea id="modal-password-input-${vaultId}" placeholder="Enter 12 Pokémon names in order: Treecko Grovyle Sceptile..." style="width: 100%; margin-bottom: 1rem; padding: 12px 16px; border: 2px solid var(--accent-primary); border-radius: 12px; min-height: 120px; resize: vertical; font-family: inherit; font-size: 0.9rem; line-height: 1.4; background: var(--bg-secondary); color: var(--text-primary); transition: border-color 0.2s ease; box-shadow: var(--shadow-soft);"></textarea>
					<div id="modal-verification-progress-${vaultId}" style="display: none; margin-bottom: 1rem; padding: 16px; background: rgba(79, 134, 200, 0.1); border-radius: 12px; border: 1px solid rgba(79, 134, 200, 0.3); box-shadow: var(--shadow-soft);">
						<div style="text-align: center; font-weight: 600; margin-bottom: 8px; color: var(--accent-secondary);">
							<i class='fas fa-spinner fa-spin'></i> Verifying Password...
						</div>
					</div>
					<div class="form-actions" style="display: flex; gap: 12px; justify-content: stretch;">
						<button class="btn btn-primary" onclick="submitModalVaultPassword('${vaultId}', '${sessionId}')" style="flex: 1; padding: 14px 20px; font-size: 0.95rem; font-weight: 600;">
							<i class='fas fa-unlock'></i> Submit
						</button>
						<button class="btn btn-outline" onclick="resetModalPokemonSelection('${vaultId}')" style="flex: 1; padding: 14px 20px; font-size: 0.95rem;">
							<i class='fas fa-redo'></i> Reset
						</button>
					</div>
				</div>
			</div>
		</div>
	`;

	modal.style.display = "block";

	setTimeout(() => {
		if (selectedPokemon.length > 0) {
			const pokemonNames = selectedPokemon.map((p) => p.name);
			const edges = [];

			visualizePokemonGraph(
				{ vertices: pokemonNames, edges },
				`modal-graph-viz-${vaultId}`,
				`modal-password-input-${vaultId}`,
			);
		}
	}, 100);
}

function closeVaultModal() {
	const modal = document.getElementById("vaultModal");
	modal.style.display = "none";
}

async function submitModalVaultPassword(vaultId, sessionId) {
	const passwordInput = document.getElementById(
		`modal-password-input-${vaultId}`,
	);
	if (!passwordInput) return;

	const solution = passwordInput.value.trim();
	if (!solution) {
		showMessage("Please enter your password", "error");
		return;
	}

	const progressDiv = document.getElementById(
		`modal-verification-progress-${vaultId}`,
	);
	const submitButton = document.querySelector(
		`button[onclick="submitModalVaultPassword('${vaultId}', '${sessionId}')"]`,
	);

	if (progressDiv) {
		progressDiv.style.display = "block";
		if (submitButton) {
			submitButton.disabled = true;
			submitButton.innerHTML =
				"<i class='fas fa-spinner fa-spin'></i> Verifying...";
		}
	}

	try {
		const response = await fetch("/api/session/verify", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				Authorization: `Bearer ${currentSessionToken}`,
			},
			body: JSON.stringify({
				password: solution,
			}),
		});

		const data = await response.json();

		if (progressDiv) {
			progressDiv.style.display = "none";
		}
		if (submitButton) {
			submitButton.disabled = false;
			submitButton.innerHTML =
				"<i class='fas fa-unlock'></i> Submit Password";
		}

		if (data.success) {
			showMessage(
				`<i class='fas fa-check-circle'></i> Vault Verification Successful! ${data.message || ""}`,
				"success",
			);
			closeVaultModal();
			closeVaultSection();
			endSession();
		} else {
			showMessage(
				data.error ||
					"❌ Verification failed! Please check your password and try again.",
				"error",
			);
		}
	} catch (error) {
		if (progressDiv) {
			progressDiv.style.display = "none";
		}
		if (submitButton) {
			submitButton.disabled = false;
			submitButton.innerHTML =
				"<i class='fas fa-unlock'></i> Submit Password";
		}
		showMessage("⚠️ Error during verification. Please try again!", "error");
	}
}

function resetModalPokemonSelection(vaultId) {
	const passwordInput = document.getElementById(
		`modal-password-input-${vaultId}`,
	);
	if (passwordInput) {
		passwordInput.value = "";
	}

	const graphContainer = document.getElementById(
		`modal-graph-viz-${vaultId}`,
	);
	if (graphContainer) {
		const svg = d3.select(`#modal-graph-viz-${vaultId}`).select("svg");
		svg.selectAll(".node")
			.classed("clicked", false)
			.transition()
			.duration(300)
			.style("opacity", 1);
		svg.selectAll(".node image").style("cursor", "pointer");
	}
}

document.addEventListener("DOMContentLoaded", function () {
	initializeApp();
	loadPokedexData();

	window.onclick = function (event) {
		const vaultModal = document.getElementById("vaultModal");
		const pokedexModal = document.getElementById("pokedexModal");

		if (event.target === vaultModal) {
			closeVaultModal();
		}
		if (event.target === pokedexModal) {
			closePokedex();
		}
	};
});
