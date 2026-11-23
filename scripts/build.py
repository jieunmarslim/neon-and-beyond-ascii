#!/usr/bin/env python3
"""Build standalone full-screen index.html for Neon and Beyond (JAPAC Cloud Techies)."""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "assets" / "cloud-logo.png"
OUT_HTML = ROOT / "index.html"

logo_b64 = base64.b64encode(LOGO_PATH.read_bytes()).decode("ascii")

HTML_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Neon and Beyond — JAPAC Cloud Techies</title>
  <meta name="description" content="Full-bleed interactive floating ASCII art canvas with 2D shallow-water ripple physics and steady wind flow. Gemini 4 Neon." />
  <!-- TODO(security): Single-file offline HTML prototype uses inline style/script; move to external bundles with server CSP nonces if deployed to production. -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=JetBrains+Mono:wght@500;600;700;800&family=Noto+Sans+KR:wght@400;500&display=swap"
  />
  <style>
    :root {
      --bg-night: #05080F;
      --dock-bg: rgba(9, 14, 24, 0.72);
      --pill-hover: rgba(255, 255, 255, 0.07);
      --pill-active: rgba(255, 255, 255, 0.14);
      --ink-primary: #F2F5FA;
      --ink-secondary: #8A9BB3;
      --focus-blue: #4285F4;
      --font-sans: 'Inter', 'Noto Sans KR', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      scrollbar-width: none;
      -ms-overflow-style: none;
    }

    *::-webkit-scrollbar {
      display: none;
    }

    html, body {
      width: 100%;
      height: 100vh;
      height: 100dvh;
      overflow: hidden;
      background: var(--bg-night);
      color: var(--ink-primary);
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
    }

    #stage {
      position: fixed;
      inset: 0;
      width: 100vw;
      height: 100vh;
      height: 100dvh;
      display: block;
      cursor: pointer;
      touch-action: none;
      user-select: none;
    }

    .footer-dock {
      position: fixed;
      left: 50%;
      bottom: max(18px, env(safe-area-inset-bottom, 18px));
      transform: translateX(-50%);
      z-index: 10;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 8px;
      max-width: calc(100vw - 24px);
      pointer-events: none;
    }

    .switcher {
      pointer-events: auto;
      display: inline-flex;
      align-items: center;
      gap: 2px;
      padding: 4px;
      border-radius: 9999px;
      background: var(--dock-bg);
      backdrop-filter: saturate(160%) blur(22px);
      -webkit-backdrop-filter: saturate(160%) blur(22px);
      box-shadow: 0 16px 44px rgba(0, 0, 0, 0.52);
      max-width: 100%;
      overflow-x: auto;
    }

    .logo-btn {
      appearance: none;
      border: 1px solid transparent;
      background: transparent;
      color: var(--ink-secondary);
      font-family: var(--font-sans);
      font-size: 12.5px;
      font-weight: 500;
      letter-spacing: -0.01em;
      line-height: 1;
      height: 33px;
      padding: 0 13px;
      border-radius: 9999px;
      cursor: pointer;
      white-space: nowrap;
      flex-shrink: 0;
      transition: background-color 160ms ease, color 160ms ease;
    }

    .logo-btn:hover {
      background: var(--pill-hover);
      color: var(--ink-primary);
    }

    .logo-btn[aria-pressed="true"] {
      background: var(--pill-active);
      color: var(--ink-primary);
    }

    .logo-btn:focus-visible {
      outline: none;
      border-color: var(--focus-blue);
    }

    .credit {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 500;
      letter-spacing: 0.03em;
      color: rgba(206, 220, 240, 0.72);
      padding: 4px 12px;
      border-radius: 9999px;
      background: rgba(5, 8, 15, 0.66);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      user-select: none;
      white-space: nowrap;
    }

    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
    }

    @media (max-width: 700px) {
      .logo-btn {
        font-size: 11.5px;
        height: 31px;
        padding: 0 10px;
      }
      .credit {
        font-size: 10px;
      }
    }
  </style>
</head>
<body>
  <h1 class="sr-only">Neon and Beyond — JAPAC Cloud Techies Full-Bleed Floating ASCII Art</h1>
  <canvas id="stage" aria-label="Full-bleed floating ASCII art with shallow-water ripple physics"></canvas>

  <footer class="footer-dock">
    <nav class="switcher" role="group" aria-label="Select floating pattern">
      <button id="btnCloud" class="logo-btn" type="button" data-logo="cloud" aria-pressed="true">Google Cloud</button>
      <button id="btnGoogle" class="logo-btn" type="button" data-logo="google" aria-pressed="false">Google</button>
      <button id="btnGemini" class="logo-btn" type="button" data-logo="gemini" aria-pressed="false">Gemini</button>
      <button id="btnMars" class="logo-btn" type="button" data-logo="mars" aria-pressed="false">Mars</button>
      <button id="btnAngel" class="logo-btn" type="button" data-logo="angel" aria-pressed="false">Angel</button>
      <button id="btnNeon" class="logo-btn" type="button" data-logo="neon" aria-pressed="false">Neon &amp; Beyond</button>
      <button id="btnJapac" class="logo-btn" type="button" data-logo="japac" aria-pressed="false">JAPAC</button>
    </nav>
    <p class="credit">Gemini 4 Neon</p>
  </footer>

  <script>
    (() => {
      "use strict";

      const CLOUD_LOGO_URI = "data:image/png;base64,__LOGO_B64__";

      const C_RED = [234, 67, 53];
      const C_YEL = [251, 188, 4];
      const C_GRN = [52, 168, 83];
      const C_BLU = [66, 133, 244];

      // Restrained winter accents (soft champagne gold & frost mist)
      const WINTER_TINTS = [
        [255, 232, 174],
        [182, 220, 255],
        [168, 232, 198],
      ];

      const canvas = document.getElementById("stage");
      const ctx = canvas.getContext("2d", { alpha: false });

      const offCanvas = document.createElement("canvas");
      const octx = offCanvas.getContext("2d", { alpha: false });

      const bloomCanvas = document.createElement("canvas");
      const bctx = bloomCanvas.getContext("2d");

      let viewW = window.innerWidth;
      let viewH = window.innerHeight;
      let dpr = Math.min(window.devicePixelRatio || 1, 2);

      // Fine editorial ASCII grid
      const CELL_W = 8;
      const CELL_H = 10;

      // =========================================================================
      // Real 2D Open-Ocean Shallow-Water Wave Equation PDE (Verlet + 28-cell PML
      // offscreen sponge + Mur Sommerfeld radiation outflow -> ZERO edge reflection!)
      // =========================================================================
      const FW_VIS = 148;
      const FH_VIS = 92;
      const F_PAD = 28;
      const FW = FW_VIS + F_PAD * 2;
      const FH = FH_VIS + F_PAD * 2;
      const F_COUNT = FW * FH;
      let hPrev = new Float32Array(F_COUNT);
      let hCurr = new Float32Array(F_COUNT);
      let hNext = new Float32Array(F_COUNT);

      const PDE_C2 = 0.18;
      const PDE_C = Math.sqrt(PDE_C2);
      const PDE_MUR = (PDE_C - 1.0) / (PDE_C + 1.0);
      const PDE_BASE_DAMP = 0.979;
      const PDE_STEP_DT = 1.0 / 45.0; // Fixed-timestep deep-water rate (~19 cells/s, refresh-rate independent)
      let fluidAcc = 0.0;
      let fluidAlpha = 1.0;

      // Precomputed open-ocean sponge damping field (uniform inside viewport, smooth quadratic absorption offscreen)
      const dampField = new Float32Array(F_COUNT);
      for (let y = 0; y < FH; y++) {
        const oy = y < F_PAD ? F_PAD - y : (y >= F_PAD + FH_VIS ? y - (F_PAD + FH_VIS - 1) : 0);
        const y0 = y * FW;
        for (let x = 0; x < FW; x++) {
          const ox = x < F_PAD ? F_PAD - x : (x >= F_PAD + FW_VIS ? x - (F_PAD + FW_VIS - 1) : 0);
          const tPad = Math.min(1.0, Math.hypot(ox, oy) / F_PAD);
          dampField[y0 + x] = PDE_BASE_DAMP * (1.0 - 0.16 * tPad * tPad);
        }
      }

      // Active water-drop origins for quick idle skip
      const surfaceDrops = [];

      // Unified calm diagonal flow: lower-left -> upper-right (+22° upward diagonal)
      const DIAG_RAD = (22.0 * Math.PI) / 180.0;
      const DIAG_X = Math.cos(DIAG_RAD);  // ~0.9272 (+x right)
      const DIAG_Y = -Math.sin(DIAG_RAD); // ~-0.3746 (-y up in 2D canvas)
      const WIND_SPEED_PX = 34.0;
      const SWELL_AMP = 11.5;

      // Subtle damped pointer parallax for gentle spatial depth
      let ptrTargetX = 0;
      let ptrTargetY = 0;
      let ptrSmoothX = 0;
      let ptrSmoothY = 0;

      function stepWaterPDE(dt) {
        fluidAcc = Math.min(fluidAcc + dt, PDE_STEP_DT * 3.0);
        while (fluidAcc >= PDE_STEP_DT) {
          fluidAcc -= PDE_STEP_DT;
          // 1. Interior 2D wave PDE with smooth offscreen open-ocean absorption
          for (let y = 1; y < FH - 1; y++) {
            const ym = (y - 1) * FW;
            const y0 = y * FW;
            const yp = (y + 1) * FW;
            for (let x = 1; x < FW - 1; x++) {
              const i = y0 + x;
              const lap =
                hCurr[i - 1] +
                hCurr[i + 1] +
                hCurr[ym + x] +
                hCurr[yp + x] -
                4.0 * hCurr[i];
              let val = (2.0 * hCurr[i] - hPrev[i] + PDE_C2 * lap) * dampField[i];
              if (val > 3.0) val = 3.0;
              else if (val < -3.0) val = -3.0;
              else if (Math.abs(val) < 1e-5) val = 0;
              hNext[i] = val;
            }
          }

          // 2. First-order Mur Sommerfeld non-reflecting outflow on all 4 outer offscreen rims
          const lastRow = (FH - 1) * FW;
          const prevRow = (FH - 2) * FW;
          for (let x = 1; x < FW - 1; x++) {
            hNext[x] = (hCurr[FW + x] + PDE_MUR * (hNext[FW + x] - hCurr[x])) * 0.84;
            hNext[lastRow + x] = (hCurr[prevRow + x] + PDE_MUR * (hNext[prevRow + x] - hCurr[lastRow + x])) * 0.84;
          }
          for (let y = 0; y < FH; y++) {
            const y0 = y * FW;
            hNext[y0] = (hCurr[y0 + 1] + PDE_MUR * (hNext[y0 + 1] - hCurr[y0])) * 0.84;
            const xr = y0 + FW - 1;
            hNext[xr] = (hCurr[xr - 1] + PDE_MUR * (hNext[xr - 1] - hCurr[xr])) * 0.84;
          }

          const tmp = hPrev;
          hPrev = hCurr;
          hCurr = hNext;
          hNext = tmp;
        }
        fluidAlpha = fluidAcc / PDE_STEP_DT;
      }

      function injectWaterDrop(sx, sy, strength = 1.0, radiusCells = 2.9) {
        const fx = F_PAD + (sx / Math.max(1, viewW)) * (FW_VIS - 1);
        const fy = F_PAD + (sy / Math.max(1, viewH)) * (FH_VIS - 1);
        const rCeil = Math.ceil(radiusCells * 2.4);
        const r2 = radiusCells * radiusCells;
        const cx = Math.round(fx);
        const cy = Math.round(fy);
        for (let dy = -rCeil; dy <= rCeil; dy++) {
          const gy = cy + dy;
          if (gy < 1 || gy >= FH - 1) continue;
          for (let dx = -rCeil; dx <= rCeil; dx++) {
            const gx = cx + dx;
            if (gx < 1 || gx >= FW - 1) continue;
            const d2 = dx * dx + dy * dy;
            if (d2 > r2 * 5.0) continue;
            const idx = gy * FW + gx;
            const drop = 1.85 * strength * Math.exp(-d2 / (2 * r2));
            hCurr[idx] -= drop;
            hPrev[idx] -= drop * 0.35;
          }
        }
        surfaceDrops.push({ x: sx, y: sy, t0: simTime, strength });
        if (surfaceDrops.length > 8) surfaceDrops.shift();
      }

      // Continuously press & hold a smooth tactile concave water bowl under the user's pointer
      function holdWaterDepression(sx, sy, depthFactor, dt, radiusCells = 3.6) {
        const fx = F_PAD + (sx / Math.max(1, viewW)) * (FW_VIS - 1);
        const fy = F_PAD + (sy / Math.max(1, viewH)) * (FH_VIS - 1);
        const rCeil = Math.ceil(radiusCells * 2.5);
        const r2 = radiusCells * radiusCells;
        const cx = Math.round(fx);
        const cy = Math.round(fy);
        const pull = 1.0 - Math.exp(-11.0 * dt);
        const calm = 1.0 - Math.exp(-14.0 * dt);
        for (let dy = -rCeil; dy <= rCeil; dy++) {
          const gy = cy + dy;
          if (gy < 1 || gy >= FH - 1) continue;
          for (let dx = -rCeil; dx <= rCeil; dx++) {
            const gx = cx + dx;
            if (gx < 1 || gx >= FW - 1) continue;
            const d2 = dx * dx + dy * dy;
            if (d2 > r2 * 5.2) continue;
            const w = Math.exp(-d2 / (2 * r2));
            const idx = gy * FW + gx;
            const targetH = -2.35 * depthFactor * w;
            // Pull fluid cleanly into a held concave hollow while softly damping inner chatter
            hCurr[idx] += (targetH - hCurr[idx]) * (pull * w);
            hPrev[idx] += (hCurr[idx] - hPrev[idx]) * (calm * w);
          }
        }
        if (surfaceDrops.length === 0) {
          surfaceDrops.push({ x: sx, y: sy, t0: simTime, strength: depthFactor });
        } else {
          const last = surfaceDrops[surfaceDrops.length - 1];
          last.x = sx;
          last.y = sy;
          last.t0 = simTime;
        }
      }

      // Energetic buoyant release rebound wave when lifting a pressed finger or submerged logo
      function releaseWaterRebound(sx, sy, strength = 1.35, radiusCells = 3.2) {
        const fx = F_PAD + (sx / Math.max(1, viewW)) * (FW_VIS - 1);
        const fy = F_PAD + (sy / Math.max(1, viewH)) * (FH_VIS - 1);
        const rCeil = Math.ceil(radiusCells * 2.5);
        const r2 = radiusCells * radiusCells;
        const cx = Math.round(fx);
        const cy = Math.round(fy);
        for (let dy = -rCeil; dy <= rCeil; dy++) {
          const gy = cy + dy;
          if (gy < 1 || gy >= FH - 1) continue;
          for (let dx = -rCeil; dx <= rCeil; dx++) {
            const gx = cx + dx;
            if (gx < 1 || gx >= FW - 1) continue;
            const d2 = dx * dx + dy * dy;
            if (d2 > r2 * 5.2) continue;
            const w = Math.exp(-d2 / (2 * r2));
            const idx = gy * FW + gx;
            // Upward spring-back crest + outward momentum launches a smooth 360° release wave
            hCurr[idx] += 1.55 * strength * w;
            hPrev[idx] -= 0.28 * strength * w;
          }
        }
        surfaceDrops.push({ x: sx, y: sy, t0: simTime, strength });
        if (surfaceDrops.length > 8) surfaceDrops.shift();
      }

      function sampleFluidPDE(sx, sy) {
        const u = Math.max(1, Math.min(FW - 2.001, F_PAD + (sx / Math.max(1, viewW)) * (FW_VIS - 1)));
        const v = Math.max(1, Math.min(FH - 2.001, F_PAD + (sy / Math.max(1, viewH)) * (FH_VIS - 1)));
        const x0 = Math.floor(u);
        const y0 = Math.floor(v);
        const x1 = x0 + 1;
        const y1 = y0 + 1;
        const tx = u - x0;
        const ty = v - y0;

        const r0 = y0 * FW;
        const r1 = y1 * FW;
        const a = fluidAlpha;
        const ia = 1.0 - a;
        const h00 = hPrev[r0 + x0] * ia + hCurr[r0 + x0] * a;
        const h10 = hPrev[r0 + x1] * ia + hCurr[r0 + x1] * a;
        const h01 = hPrev[r1 + x0] * ia + hCurr[r1 + x0] * a;
        const h11 = hPrev[r1 + x1] * ia + hCurr[r1 + x1] * a;

        const h =
          (h00 * (1 - tx) + h10 * tx) * (1 - ty) +
          (h01 * (1 - tx) + h11 * tx) * ty;

        const gx = ((hPrev[r0 + x1] - hPrev[r0 + x0 - 1]) * ia + (hCurr[r0 + x1] - hCurr[r0 + x0 - 1]) * a) * 0.5;
        const gy = ((hPrev[r1 + x0] - hPrev[(y0 - 1) * FW + x0]) * ia + (hCurr[r1 + x0] - hCurr[(y0 - 1) * FW + x0]) * a) * 0.5;
        return { h, gx, gy };
      }

      function evalWindSwell(alongDiag, t) {
        const k = (Math.PI * 2 * 1.8) / Math.max(1, Math.hypot(viewW, viewH));
        const phase = alongDiag * k - t * 0.68;
        const h = SWELL_AMP * (Math.sin(phase) + 0.10 * Math.sin(2 * phase));
        const slope = SWELL_AMP * k * (Math.cos(phase) + 0.20 * Math.cos(2 * phase));
        return { h, slope };
      }

      // =========================================================================
      // Full-Bleed Continuous Diagonal Buoyant Lattice + Restrained Far Depth Layer
      // =========================================================================
      let bodies = [];
      let bgBodies = [];
      let numCols = 3;
      let numRows = 4;
      let TILE_W = 480;
      let TILE_H = 310;
      let SPAN_X = 1440;
      let SPAN_Y = 1240;
      let Y_PAD = 170;
      let OBJ_DRAW_W = 355;

      let BG_SPAN_X = 1440;
      let BG_SPAN_Y = 1240;
      let BG_Y_PAD = 170;
      let BG_DRAW_W = 195;

      function rebuildBodies() {
        const isHeroMars = activeLogo === "mars";
        const isBanner = activeLogo === "neon" || activeLogo === "japac";
        const compact = Math.min(viewW, viewH) < 680;

        if (isHeroMars) {
          // Dedicated solo space centerpiece: one monumental slowly-rotating 3D Mars in deep space
          numCols = 1;
          numRows = 1;
          TILE_W = viewW;
          TILE_H = viewH;
          SPAN_X = viewW;
          SPAN_Y = viewH;
          Y_PAD = 0;
          OBJ_DRAW_W = Math.round(Math.min(viewW * 0.72, viewH * 0.72, 580));
          const cx = viewW * 0.5;
          const cy = viewH * 0.47;
          bodies = [{
            row: 0,
            col: 0,
            laneX: cx,
            laneY: cy,
            x: cx,
            y: cy,
            heave: 0,
            vHeave: 0,
            surgeX: 0,
            vSurgeX: 0,
            surgeY: 0,
            vSurgeY: 0,
            bobScale: 1,
            angle: 0,
            omega: 0,
            sink: 0,
            vSink: 0,
            tiltX: 0,
            vTiltX: 0,
            tiltY: 0,
            vTiltY: 0,
          }];
          bgBodies = [];
          pressedBody = null;
          pressHold = 0;
          return;
        }

        if (isBanner) {
          numCols = Math.max(1, Math.round(viewW / (compact ? 420 : 660)));
          TILE_W = viewW / numCols;
          TILE_H = compact ? 248 : 332;
          OBJ_DRAW_W = Math.min(TILE_W * 0.86, compact ? 375 : 590);
        } else {
          numCols = Math.max(2, Math.round(viewW / (compact ? 310 : 470)));
          TILE_W = viewW / numCols;
          TILE_H = compact ? 255 : 318;
          OBJ_DRAW_W = Math.min(TILE_W * 0.78, compact ? 245 : 352);
        }

        // Enforce even row count so half-cell horizontal stagger wraps seamlessly across top/bottom edges
        numRows = Math.max(4, Math.ceil((viewH + TILE_H) / TILE_H));
        if (numRows & 1) numRows += 1;
        SPAN_X = numCols * TILE_W;
        SPAN_Y = numRows * TILE_H;
        Y_PAD = (SPAN_Y - viewH) * 0.5;

        const nextBodies = [];
        const startY = TILE_H * 0.08;
        for (let r = 0; r < numRows; r++) {
          const stagger = (r & 1) ? TILE_W * 0.5 : 0;
          const baseY = modPos(startY + r * TILE_H + Y_PAD, SPAN_Y) - Y_PAD;
          for (let c = 0; c < numCols; c++) {
            const baseX = modPos((c + 0.5) * TILE_W + stagger, SPAN_X);
            nextBodies.push({
              row: r,
              col: c,
              laneX: baseX,
              laneY: baseY,
              x: baseX,
              y: baseY,
              heave: 0,
              vHeave: 0,
              surgeX: 0,
              vSurgeX: 0,
              surgeY: 0,
              vSurgeY: 0,
              bobScale: 1,
              angle: 0,
              omega: 0,
              sink: 0,
              vSink: 0,
              tiltX: 0,
              vTiltX: 0,
              tiltY: 0,
              vTiltY: 0,
            });
          }
        }
        bodies = nextBodies;
        pressedBody = null;
        pressHold = 0;

        // ONE restrained, faint far-background parallax layer (~0.55x scale, independent frequency so it floats in open space rather than mirroring as a shadow)
        const bgCols = numCols + 1;
        const exactBgTileW = viewW / bgCols;
        const bgTileH = TILE_H * 0.76;
        let bgRows = Math.max(6, Math.ceil((viewH + bgTileH) / bgTileH));
        if (bgRows & 1) bgRows += 1;

        BG_SPAN_X = bgCols * exactBgTileW;
        BG_SPAN_Y = bgRows * bgTileH;
        BG_Y_PAD = (BG_SPAN_Y - viewH) * 0.5;
        BG_DRAW_W = OBJ_DRAW_W * 0.54;

        const nextBg = [];
        for (let r = 0; r < bgRows; r++) {
          const stagger = (r & 1) ? exactBgTileW * 0.5 : 0;
          const baseY = modPos(bgTileH * 0.52 + r * bgTileH + BG_Y_PAD, BG_SPAN_Y) - BG_Y_PAD;
          for (let c = 0; c < bgCols; c++) {
            // Subtle deterministic organic jitter within each far cell so background depth feels natural
            const jx = (Math.sin(r * 19.3 + c * 31.7) * 0.14) * exactBgTileW;
            const jy = (Math.cos(r * 23.1 + c * 17.9) * 0.14) * bgTileH;
            const baseX = modPos((c + 0.22) * exactBgTileW + stagger + jx, BG_SPAN_X);
            const cellY = modPos(baseY + jy + BG_Y_PAD, BG_SPAN_Y) - BG_Y_PAD;
            nextBg.push({
              laneX: baseX,
              laneY: cellY,
              x: baseX,
              y: cellY,
              surgeX: 0,
              vSurgeX: 0,
              surgeY: 0,
              vSurgeY: 0,
              bobScale: 1,
              angle: 0,
              omega: 0,
            });
          }
        }
        bgBodies = nextBg;
      }

      // Pointer press-and-hold interaction state (sinking water hollow + asymmetric logo submersion)
      let pointerDown = false;
      let lastDragX = 0, lastDragY = 0;
      let pressX = 0, pressY = 0;
      let pressStartTime = 0;
      let pressHold = 0;
      let pressedBody = null;
      let pressU = 0, pressV = 0;
      let pressWrapDx = 0, pressWrapDy = 0;

      // Dedicated Hero Mars deep-space state: spacecraft camera orbiting Mars (distant Sun at infinity, always behind Mars when visible)
      const MARS_BASE_SPIN = 0.085;  // serene ~74s per axial revolution
      const MARS_SUN_SPEED = 0.095;  // slow ~66s per full 360° camera-orbit phase cycle
      let marsSpinAngle = 0.35;
      let marsSpinVel = MARS_BASE_SPIN;
      let marsSunAngle = Math.PI * 0.92; // opens in classic sunlit gibbous phase; Sun soon glides in from left edge
      const marsMeteors = [];
      let nextAmbientMeteorAt = 4.5;

      function spawnMarsMeteor(sx, sy, isAmbient) {
        const goRight = sx < viewW * 0.52;
        const baseDeg = goRight ? (25 + Math.random() * 14) : (141 + Math.random() * 14);
        const rad = (baseDeg * Math.PI) / 180.0;
        const speed = isAmbient ? (380 + Math.random() * 120) : (470 + Math.random() * 140);
        const warm = Math.random() < 0.45;
        marsMeteors.push({
          x: sx,
          y: sy,
          vx: Math.cos(rad) * speed,
          vy: Math.sin(rad) * speed,
          dirX: Math.cos(rad),
          dirY: Math.sin(rad),
          age: 0,
          life: isAmbient ? (0.85 + Math.random() * 0.35) : (0.95 + Math.random() * 0.35),
          tailLen: isAmbient ? (115 + Math.random() * 45) : (165 + Math.random() * 60),
          peakAlpha: isAmbient ? 0.58 : 0.94,
          tint: warm ? [255, 224, 166] : [196, 224, 255],
          seed: Math.random() * 100.0,
        });
        if (marsMeteors.length > 14) marsMeteors.shift();
      }

      function updateMarsSunVector() {
        const sCos = Math.cos(marsSunAngle);
        const sSin = Math.sin(marsSunAngle);
        const rawSX = sCos;
        const rawSY = -0.11 * sCos - 0.05; // gentle ~6° ecliptic tilt
        const rawSZ = sSin; // < 0: Sun is far behind Mars (in camera FOV); > 0: Sun is behind camera (full sunlit Mars)
        const sLen = Math.hypot(rawSX, rawSY, rawSZ) || 1.0;
        MARS_SUN[0] = rawSX / sLen;
        MARS_SUN[1] = rawSY / sLen;
        MARS_SUN[2] = rawSZ / sLen;
      }

      function stepBuoyantBodies(dt, t) {
        const ptrLerp = 1.0 - Math.exp(-3.4 * dt);
        ptrSmoothX += (ptrTargetX - ptrSmoothX) * ptrLerp;
        ptrSmoothY += (ptrTargetY - ptrSmoothY) * ptrLerp;

        const isHeroMars = activeLogo === "mars";
        if (isHeroMars) {
          const draggingMars = pointerDown && pressedBody !== null;
          const scrubbingSun = pointerDown && pressedBody === null;
          if (!draggingMars) {
            marsSpinVel += (MARS_BASE_SPIN - marsSpinVel) * (1.0 - Math.exp(-2.2 * dt));
            marsSpinAngle += marsSpinVel * dt;
          }
          if (!scrubbingSun) {
            marsSunAngle += MARS_SUN_SPEED * dt;
          }
          updateMarsSunVector();

          // Pure weightless deep-space anchor (zero water waves, zero sinking, zero water surge)
          if (bodies.length > 0) {
            const b = bodies[0];
            b.laneX = viewW * 0.5;
            b.laneY = viewH * 0.47;
            b.x = b.laneX;
            b.y = b.laneY + Math.sin(t * 0.55) * 4.0;
            b.heave = 0; b.vHeave = 0;
            b.surgeX = 0; b.vSurgeX = 0;
            b.surgeY = 0; b.vSurgeY = 0;
            b.sink = 0; b.vSink = 0;
            b.tiltX = 0; b.vTiltX = 0;
            b.tiltY = 0; b.vTiltY = 0;
            b.angle = 0; b.omega = 0;
            b.bobScale = 1.0;
          }
          pressHold = 0;
          return;
        }

        // Smoothly ramp press-and-hold depth while pointer is held down & depress water underneath
        if (pointerDown) {
          pressHold += (1.0 - pressHold) * (1.0 - Math.exp(-4.6 * dt));
          if (pressedBody) {
            // While holding a logo down, gently depress water right around the pressed side of the logo
            holdWaterDepression(pressX, pressY, 0.35 + pressHold * 0.72, dt, 3.4);
          } else {
            // While holding open water, carve a tactile concave dimple right beneath the pointer
            holdWaterDepression(pressX, pressY, 0.38 + pressHold * 0.92, dt, 3.8);
          }
        } else {
          pressHold = 0;
        }

        const vx = WIND_SPEED_PX * DIAG_X;
        const vy = WIND_SPEED_PX * DIAG_Y;
        const hullSpanX = OBJ_DRAW_W * 0.34;
        const hullSpanY = OBJ_DRAW_W * 0.24;

        for (let i = 0; i < bodies.length; i++) {
          const b = bodies[i];
          const isHeld = pointerDown && b === pressedBody;

          // 1. Steady unified diagonal drift (gently pinned under the user's hand while held down)
          const driftScale = isHeld ? Math.max(0.10, 1.0 - pressHold * 0.90) : 1.0;
          b.laneX = modPos(b.laneX + vx * driftScale * dt, SPAN_X);
          b.laneY = modPos(b.laneY + vy * driftScale * dt + Y_PAD, SPAN_Y) - Y_PAD;

          // 2. Multi-point hull wave sampling (center + 4 hull edges) for authentic buoyant surge, heave & torque
          const alongDiag = b.laneX * DIAG_X + b.laneY * DIAG_Y;
          const swell = evalWindSwell(alongDiag, t);
          const pC = sampleFluidPDE(b.laneX, b.laneY);
          const pL = sampleFluidPDE(b.laneX - hullSpanX, b.laneY);
          const pR = sampleFluidPDE(b.laneX + hullSpanX, b.laneY);
          const pT = sampleFluidPDE(b.laneX, b.laneY - hullSpanY);
          const pB = sampleFluidPDE(b.laneX, b.laneY + hullSpanY);

          const avgH = (pC.h * 2 + pL.h + pR.h + pT.h + pB.h) / 6;
          const avgGx = (pC.gx * 2 + pL.gx + pR.gx + pT.gx + pB.gx) / 6;
          const avgGy = (pC.gy * 2 + pL.gy + pR.gy + pT.gy + pB.gy) / 6;
          const hullTiltX = (pR.h - pL.h) * 0.5;
          const hullTiltY = (pB.h - pT.h) * 0.5;

          // 3. Natural underdamped 2D orbital wave surge + heave
          const targetHeave = swell.h + avgH * 24.0;
          const aHeave = 13.5 * (targetHeave - b.heave) - 3.8 * b.vHeave;
          b.vHeave += aHeave * dt;
          b.heave += b.vHeave * dt;

          const surgeScale = isHeld ? 0.25 : 1.0;
          const targetSurgeX = Math.max(-44, Math.min(44, -avgGx * 105.0 * surgeScale));
          const targetSurgeY = Math.max(-44, Math.min(44, (-avgGy * 105.0 - avgH * 18.0) * surgeScale));
          b.vSurgeX += (15.0 * (targetSurgeX - b.surgeX) - 3.6 * b.vSurgeX) * dt;
          b.surgeX += b.vSurgeX * dt;
          b.vSurgeY += (15.0 * (targetSurgeY - b.surgeY) - 3.6 * b.vSurgeY) * dt;
          b.surgeY += b.vSurgeY * dt;

          b.x = b.laneX - DIAG_Y * b.heave * 0.35 + b.surgeX;
          b.y = b.laneY + DIAG_X * b.heave + b.surgeY;

          // 4. Tactile 3D submersion & asymmetric side-tilt when pressed by hand
          const targetSink = isHeld ? (0.28 + pressHold * 0.76) : 0.0;
          const sinkK = isHeld ? 24.0 : 17.5;
          const sinkDamp = isHeld ? 7.2 : 3.4;
          b.vSink += (sinkK * (targetSink - b.sink) - sinkDamp * b.vSink) * dt;
          b.sink = Math.max(-0.26, Math.min(1.18, b.sink + b.vSink * dt));

          const targetTiltY = isHeld
            ? Math.max(-0.56, Math.min(0.56, pressU * (0.44 + pressHold * 0.16)))
            : Math.max(-0.24, Math.min(0.24, -hullTiltX * 0.32));
          const targetTiltX = isHeld
            ? Math.max(-0.54, Math.min(0.54, pressV * (0.42 + pressHold * 0.16)))
            : Math.max(-0.24, Math.min(0.24, -hullTiltY * 0.32));
          const tiltK = isHeld ? 22.0 : 14.5;
          const tiltDamp = isHeld ? 6.6 : 3.2;
          b.vTiltY += (tiltK * (targetTiltY - b.tiltY) - tiltDamp * b.vTiltY) * dt;
          b.tiltY += b.vTiltY * dt;
          b.vTiltX += (tiltK * (targetTiltX - b.tiltX) - tiltDamp * b.vTiltX) * dt;
          b.tiltX += b.vTiltX * dt;

          // Subtle 2.5D depth lift scale as wave crest raises/lowers the floating object
          const targetScale = 1.0 + Math.max(-0.055, Math.min(0.08, avgH * 0.075));
          b.bobScale += (targetScale - b.bobScale) * Math.min(1, dt * 6.0);

          // 5. Physical buoyant rocking torque across the wave slope (up to ~14° on nearby splashes)
          const rawAngle = swell.slope * 0.34 + hullTiltX * 0.45 - avgGx * 0.58 + (isHeld ? pressU * pressV * 0.14 : 0);
          const targetAngle = Math.max(-0.24, Math.min(0.24, rawAngle));
          const alpha = 14.5 * (targetAngle - b.angle) - 3.4 * b.omega;
          b.omega += alpha * dt;
          b.angle += b.omega * dt;
        }

        // Far-background layer drifts at 0.48x speed AND responds sympathetically to passing waves
        const bgVx = vx * 0.48;
        const bgVy = vy * 0.48;
        for (let i = 0; i < bgBodies.length; i++) {
          const bg = bgBodies[i];
          bg.laneX = modPos(bg.laneX + bgVx * dt, BG_SPAN_X);
          bg.laneY = modPos(bg.laneY + bgVy * dt + BG_Y_PAD, BG_SPAN_Y) - BG_Y_PAD;
          const alongDiag = bg.laneX * DIAG_X + bg.laneY * DIAG_Y;
          const swell = evalWindSwell(alongDiag * 0.7, t * 0.72);
          const pde = sampleFluidPDE(bg.laneX, bg.laneY);

          const bgTargetSX = Math.max(-24, Math.min(24, -pde.gx * 58.0));
          const bgTargetSY = Math.max(-24, Math.min(24, -pde.gy * 58.0 - pde.h * 12.0));
          bg.vSurgeX += (12.0 * (bgTargetSX - bg.surgeX) - 3.4 * bg.vSurgeX) * dt;
          bg.surgeX += bg.vSurgeX * dt;
          bg.vSurgeY += (12.0 * (bgTargetSY - bg.surgeY) - 3.4 * bg.vSurgeY) * dt;
          bg.surgeY += bg.vSurgeY * dt;

          bg.x = bg.laneX - DIAG_Y * swell.h * 0.16 + bg.surgeX;
          bg.y = bg.laneY + DIAG_X * swell.h * 0.45 + bg.surgeY;

          const bgTargetScale = 1.0 + Math.max(-0.035, Math.min(0.05, pde.h * 0.045));
          bg.bobScale += (bgTargetScale - bg.bobScale) * Math.min(1, dt * 5.5);

          const bgTargetAngle = Math.max(-0.15, Math.min(0.15, swell.slope * 0.18 - pde.gx * 0.34));
          bg.omega += (12.0 * (bgTargetAngle - bg.angle) - 3.2 * bg.omega) * dt;
          bg.angle += bg.omega * dt;
        }
      }

      function updateLayoutMetrics() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        dpr = Math.min(window.devicePixelRatio || 1, 2);

        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        canvas.style.width = `${viewW}px`;
        canvas.style.height = `${viewH}px`;

        offCanvas.width = Math.round(viewW * dpr);
        offCanvas.height = Math.round(viewH * dpr);

        bloomCanvas.width = Math.max(120, Math.round(viewW * 0.25));
        bloomCanvas.height = Math.max(120, Math.round(viewH * 0.25));

        rebuildBodies();
      }

      function mulberry32(seed) {
        let a = seed >>> 0;
        return () => {
          a |= 0;
          a = (a + 0x6D2B79F5) | 0;
          let t = Math.imul(a ^ (a >>> 15), 1 | a);
          t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
          return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        };
      }

      function modPos(a, n) {
        return ((a % n) + n) % n;
      }

      function lerpColor(a, b, t) {
        const c = Math.max(0, Math.min(1, t));
        return [
          a[0] + (b[0] - a[0]) * c,
          a[1] + (b[1] - a[1]) * c,
          a[2] + (b[2] - a[2]) * c,
        ];
      }

      function sampleGoogleWheel(ang) {
        const stops = [
          [-Math.PI, C_YEL],
          [-2.35, C_RED],
          [-0.78, C_RED],
          [-0.08, C_BLU],
          [0.72, C_BLU],
          [1.48, C_GRN],
          [2.32, C_GRN],
          [2.95, C_YEL],
          [Math.PI, C_YEL],
        ];
        for (let i = 0; i < stops.length - 1; i++) {
          const [a0, c0] = stops[i];
          const [a1, c1] = stops[i + 1];
          if (ang >= a0 && ang <= a1) {
            const t = (ang - a0) / Math.max(1e-5, a1 - a0);
            const s = t * t * (3 - 2 * t);
            return lerpColor(c0, c1, s);
          }
        }
        return C_BLU;
      }

      function exactEdt2D(mask, w, h) {
        const INF = 1e9;
        const f = new Float64Array(w * h);
        for (let i = 0; i < w * h; i++) f[i] = mask[i] ? INF : 0;

        const maxDim = Math.max(w, h);
        const v = new Int32Array(maxDim);
        const z = new Float64Array(maxDim + 1);
        const lineIn = new Float64Array(maxDim);
        const lineOut = new Float64Array(maxDim);

        function edt1D(n) {
          let k = 0;
          v[0] = 0;
          z[0] = -INF;
          z[1] = INF;
          for (let q = 1; q < n; q++) {
            const fq = lineIn[q];
            let s = 0;
            while (true) {
              const vk = v[k];
              s = ((fq + q * q) - (lineIn[vk] + vk * vk)) / (2 * (q - vk));
              if (s <= z[k]) k--;
              else break;
            }
            k++;
            v[k] = q;
            z[k] = s;
            z[k + 1] = INF;
          }
          k = 0;
          for (let q = 0; q < n; q++) {
            while (z[k + 1] < q) k++;
            const dq = q - v[k];
            lineOut[q] = dq * dq + lineIn[v[k]];
          }
        }

        const tmp = new Float64Array(w * h);
        for (let y = 0; y < h; y++) {
          const row = y * w;
          for (let x = 0; x < w; x++) lineIn[x] = f[row + x];
          edt1D(w);
          for (let x = 0; x < w; x++) tmp[row + x] = lineOut[x];
        }

        const dist = new Float32Array(w * h);
        for (let x = 0; x < w; x++) {
          for (let y = 0; y < h; y++) lineIn[y] = tmp[y * w + x];
          edt1D(h);
          for (let y = 0; y < h; y++) dist[y * w + x] = Math.sqrt(Math.max(0, lineOut[y]));
        }
        return dist;
      }

      function buildSurfaceFromMask(w, h, mask, rgbFlat, word, aspect, boostSat = true) {
        const dist = exactEdt2D(mask, w, h);
        const inside = [];
        for (let i = 0; i < w * h; i++) {
          if (mask[i]) inside.push(dist[i]);
        }
        inside.sort((a, b) => a - b);
        const radius = inside[Math.floor(inside.length * 0.95)] || 1;

        const nx = new Float32Array(w * h);
        const ny = new Float32Array(w * h);
        const nz = new Float32Array(w * h);
        const edge = new Float32Array(w * h);
        const rgb = new Float32Array(w * h * 3);

        for (let y = 1; y < h - 1; y++) {
          for (let x = 1; x < w - 1; x++) {
            const idx = y * w + x;
            if (!mask[idx]) continue;

            const tVal = Math.min(1, dist[idx] / radius);
            edge[idx] = tVal;
            const gx = (dist[idx + 1] - dist[idx - 1]) * 0.5;
            const gy = (dist[idx + w] - dist[idx - w]) * 0.5;
            const gl = Math.hypot(gx, gy) + 1e-6;
            const domeNz = Math.min(1, Math.max(0.26, 0.44 + 0.56 * tVal));
            const xyW = Math.sqrt(Math.max(0, 1 - domeNz * domeNz));

            nx[idx] = (-gx / gl) * xyW;
            ny[idx] = (-gy / gl) * xyW;
            nz[idx] = domeNz;

            const r = rgbFlat[idx * 3];
            const g = rgbFlat[idx * 3 + 1];
            const b = rgbFlat[idx * 3 + 2];
            if (boostSat) {
              // Refined silky official tones (vivid without harsh gaming-neon clipping)
              const gray = 0.299 * r + 0.587 * g + 0.114 * b;
              rgb[idx * 3] = Math.min(255, Math.max(0, (gray + (r - gray) * 1.12) * 1.04 + 6));
              rgb[idx * 3 + 1] = Math.min(255, Math.max(0, (gray + (g - gray) * 1.12) * 1.05 + 8));
              rgb[idx * 3 + 2] = Math.min(255, Math.max(0, (gray + (b - gray) * 1.12) * 1.07 + 10));
            } else {
              rgb[idx * 3] = r;
              rgb[idx * 3 + 1] = g;
              rgb[idx * 3 + 2] = b;
            }
          }
        }
        // Compute hole-filled outer silhouette mask (BFS from 4 border edges) so waves stay cleanly outside hollow logos
        const ext = new Uint8Array(w * h);
        const queue = new Int32Array(w * h);
        let qHead = 0;
        let qTail = 0;
        const pushExt = (px, py) => {
          const k = py * w + px;
          if (!mask[k] && !ext[k]) {
            ext[k] = 1;
            queue[qTail++] = k;
          }
        };
        for (let x = 0; x < w; x++) {
          pushExt(x, 0);
          pushExt(x, h - 1);
        }
        for (let y = 0; y < h; y++) {
          pushExt(0, y);
          pushExt(w - 1, y);
        }
        while (qHead < qTail) {
          const cur = queue[qHead++];
          const cx = cur % w;
          const cy = (cur / w) | 0;
          if (cx > 0) pushExt(cx - 1, cy);
          if (cx + 1 < w) pushExt(cx + 1, cy);
          if (cy > 0) pushExt(cx, cy - 1);
          if (cy + 1 < h) pushExt(cx, cy + 1);
        }
        const solidMask = new Uint8Array(w * h);
        for (let i = 0; i < w * h; i++) {
          solidMask[i] = ext[i] ? 0 : 1;
        }
        return { w, h, mask, solidMask, nx, ny, nz, edge, rgb, word, aspect };
      }

      // 1. Official Google Cloud 2025 gradient logo
      function buildCloudTexture(img) {
        const tmpC = document.createElement("canvas");
        tmpC.width = img.width;
        tmpC.height = img.height;
        const tctx = tmpC.getContext("2d");
        tctx.drawImage(img, 0, 0);
        const raw = tctx.getImageData(0, 0, img.width, img.height).data;

        let minX = img.width, maxX = 0, minY = img.height, maxY = 0;
        for (let y = 0; y < img.height; y++) {
          for (let x = 0; x < img.width; x++) {
            if (raw[(y * img.width + x) * 4 + 3] > 20) {
              if (x < minX) minX = x;
              if (x > maxX) maxX = x;
              if (y < minY) minY = y;
              if (y > maxY) maxY = y;
            }
          }
        }
        const pad = 3;
        minX = Math.max(0, minX - pad);
        minY = Math.max(0, minY - pad);
        maxX = Math.min(img.width - 1, maxX + pad);
        maxY = Math.min(img.height - 1, maxY + pad);
        const cw = maxX - minX + 1;
        const ch = maxY - minY + 1;

        const w = 180;
        const h = Math.round((w * ch) / cw);
        const resC = document.createElement("canvas");
        resC.width = w;
        resC.height = h;
        const rctx = resC.getContext("2d");
        rctx.drawImage(img, minX, minY, cw, ch, 0, 0, w, h);
        const data = rctx.getImageData(0, 0, w, h).data;

        const mask = new Uint8Array(w * h);
        const rgbFlat = new Float32Array(w * h * 3);
        for (let i = 0; i < w * h; i++) {
          if (data[i * 4 + 3] > 125) {
            mask[i] = 1;
            rgbFlat[i * 3] = data[i * 4];
            rgbFlat[i * 3 + 1] = data[i * 4 + 1];
            rgbFlat[i * 3 + 2] = data[i * 4 + 2];
          }
        }
        return buildSurfaceFromMask(w, h, mask, rgbFlat, "GOOGLECLOUD", ch / cw, true);
      }

      // Official 2025 Google "G" silhouette clip path (transform in 268.1522 x 273.8827)
      const GOOGLE_G_2025_PATH =
        "M371.3784 193.2406H237.0825v53.4375h77.167c-1.2405 7.5627-4.0259 15.0024-8.1049 21.7862-4.6734 7.7723-10.4511 13.6895-16.373 18.1957-17.7389 13.4983-38.42 16.2584-52.7828 16.2584-36.2824 0-67.2833-23.2865-79.2844-54.9287-.4843-1.1482-.8059-2.3344-1.1975-3.5068-2.652-8.0533-4.101-16.5825-4.101-25.4474 0-9.226 1.5691-18.0575 4.4301-26.3985 11.2851-32.8967 42.9849-57.4674 80.1789-57.4674 7.4811 0 14.6854.8843 21.5173 2.6481 15.6135 4.0309 26.6578 11.9698 33.4252 18.2494l40.834-39.7111c-24.839-22.616-57.2194-36.3201-95.8444-36.3201-30.8782-.00066-59.3863 9.55308-82.7477 25.6992-18.9454 13.0941-34.4833 30.6254-44.9695 50.9861-9.75366 18.8785-15.09441 39.7994-15.09441 62.2934 0 22.495 5.34891 43.6334 15.10261 62.3374v.126c10.3023 19.8567 25.3678 36.9537 43.6783 49.9878 15.9962 11.3866 44.6789 26.5516 84.0307 26.5516 22.6301 0 42.6867-4.0517 60.3748-11.6447 12.76-5.4775 24.0655-12.6217 34.3012-21.8036 13.5247-12.1323 24.1168-27.1388 31.3465-44.4041 7.2297-17.2654 11.097-36.7895 11.097-57.957 0-9.858-.9971-19.8694-2.6881-28.9684Z";

      // Official 2025 Google Gemini 4-point spark path (viewBox 0 0 65 65, rounded tips + smooth concavities)
      const GEMINI_2025_PATH =
        "M32.447 0c.68 0 1.273.465 1.439 1.125a38.904 38.904 0 001.999 5.905c2.152 5 5.105 9.376 8.854 13.125 3.751 3.75 8.126 6.703 13.125 8.855a38.98 38.98 0 005.906 1.999c.66.166 1.124.758 1.124 1.438 0 .68-.464 1.273-1.125 1.439a38.902 38.902 0 00-5.905 1.999c-5 2.152-9.375 5.105-13.125 8.854-3.749 3.751-6.702 8.126-8.854 13.125a38.973 38.973 0 00-2 5.906 1.485 1.485 0 01-1.438 1.124c-.68 0-1.272-.464-1.438-1.125a38.913 38.913 0 00-2-5.905c-2.151-5-5.103-9.375-8.854-13.125-3.75-3.749-8.125-6.702-13.125-8.854a38.973 38.973 0 00-5.905-2A1.485 1.485 0 010 32.448c0-.68.465-1.272 1.125-1.438a38.903 38.903 0 005.905-2c5-2.151 9.376-5.104 13.125-8.854 3.75-3.749 6.703-8.125 8.855-13.125a38.972 38.972 0 001.999-5.905A1.485 1.485 0 0132.447 0z";

      // 2. Official 2025 Google "G" circular 4-color gradient logo
      function buildGoogleTexture() {
        const w = 200, h = 200;
        const paintC = document.createElement("canvas");
        paintC.width = w;
        paintC.height = h;
        const g = paintC.getContext("2d");
        g.clearRect(0, 0, w, h);

        const vbW = 268.1522;
        const vbH = 273.8827;
        const pad = 10;
        const fitScale = (w - pad * 2) / Math.max(vbW, vbH);
        const offX = (w - vbW * fitScale) * 0.5;
        const offY = (h - vbH * fitScale) * 0.5;

        const gPath = new Path2D(GOOGLE_G_2025_PATH);
        g.save();
        g.translate(offX, offY);
        g.scale(fitScale, fitScale);
        g.transform(0.957922, 0, 0, 0.985255, -90.17436, -78.85577);
        g.fillStyle = "#FFFFFF";
        g.fill(gPath);
        g.restore();

        const maskData = g.getImageData(0, 0, w, h).data;
        const mask = new Uint8Array(w * h);
        const rgbFlat = new Float32Array(w * h * 3);

        const gStops = [
          [-Math.PI, [255, 210, 22]],
          [-2.58, [255, 144, 34]],
          [-2.08, [255, 82, 68]],
          [-1.18, [255, 76, 72]],
          [-0.70, [255, 86, 98]],
          [-0.20, [58, 146, 255]],
          [0.58, [58, 146, 255]],
          [0.98, [22, 168, 210]],
          [1.36, [24, 198, 114]],
          [1.92, [28, 200, 108]],
          [2.38, [122, 206, 28]],
          [2.78, [252, 212, 24]],
          [Math.PI, [255, 210, 22]],
        ];

        function sampleOfficialGWheel(ang) {
          for (let i = 0; i < gStops.length - 1; i++) {
            const [a0, c0] = gStops[i];
            const [a1, c1] = gStops[i + 1];
            if (ang >= a0 && ang <= a1) {
              const t = (ang - a0) / Math.max(1e-5, a1 - a0);
              const s = t * t * (3 - 2 * t);
              return lerpColor(c0, c1, s);
            }
          }
          return [58, 146, 255];
        }

        const cx = offX + (237.0825 * 0.957922 - 90.17436) * fitScale;
        const cy = offY + (219.9585 * 0.985255 - 78.85577) * fitScale;

        for (let y = 0; y < h; y++) {
          for (let x = 0; x < w; x++) {
            const idx = y * w + x;
            if (maskData[idx * 4 + 3] <= 115) continue;
            mask[idx] = 1;
            const dx = x - cx;
            const dy = y - cy;
            const ang = Math.atan2(dy, dx);
            const inBar = dx >= -3 && dy >= -22 && dy <= 22;
            const col = inBar ? [58, 146, 255] : sampleOfficialGWheel(ang);
            rgbFlat[idx * 3] = col[0];
            rgbFlat[idx * 3 + 1] = col[1];
            rgbFlat[idx * 3 + 2] = col[2];
          }
        }
        return buildSurfaceFromMask(w, h, mask, rgbFlat, "GOOGLE", 1.0, false);
      }

      // 3. Official 2025 Gemini concave 4-point sparkle logo (exact Path2D + 4-color gradient)
      function buildGeminiTexture() {
        const w = 200, h = 200;
        const paintC = document.createElement("canvas");
        paintC.width = w;
        paintC.height = h;
        const g = paintC.getContext("2d");
        g.clearRect(0, 0, w, h);

        const pad = 7;
        const scale = (w - pad * 2) / 65.0;
        const sparkPath = new Path2D(GEMINI_2025_PATH);

        function paintCloud(cx, cy, rx, ry, rotRad, stops) {
          g.save();
          g.translate(cx, cy);
          g.rotate(rotRad);
          g.scale(1, ry / Math.max(1e-4, rx));
          const grad = g.createRadialGradient(0, 0, 0, 0, 0, rx);
          for (let i = 0; i < stops.length; i++) {
            grad.addColorStop(stops[i][0], stops[i][1]);
          }
          g.fillStyle = grad;
          g.beginPath();
          g.arc(0, 0, rx, 0, Math.PI * 2);
          g.fill();
          g.restore();
        }

        g.save();
        g.translate(pad, pad);
        g.scale(scale, scale);
        g.clip(sparkPath);

        // Dominant 2025 Gemini Google Blue foundation (right tip, center core & right shoulders)
        const baseGrad = g.createLinearGradient(12, 46, 56, 16);
        baseGrad.addColorStop(0.0, "#348AFF");
        baseGrad.addColorStop(0.55, "#3C92FF");
        baseGrad.addColorStop(1.0, "#62A6FF");
        g.fillStyle = baseGrad;
        g.fillRect(-10, -10, 85, 85);

        // Bottom Emerald Green bloom (#00B95C)
        paintCloud(22.0, 58.0, 29, 31, -0.18, [
          [0.0, "rgba(12, 206, 112, 1.0)"],
          [0.48, "rgba(10, 198, 106, 0.96)"],
          [0.76, "rgba(26, 186, 128, 0.38)"],
          [1.0, "rgba(12, 206, 112, 0.0)"],
        ]);

        // Top Coral-Red bloom (#FC413D)
        paintCloud(26.5, 4.0, 29, 27, -0.35, [
          [0.0, "rgba(255, 76, 72, 1.0)"],
          [0.50, "rgba(255, 72, 68, 0.96)"],
          [0.78, "rgba(250, 96, 94, 0.34)"],
          [1.0, "rgba(255, 76, 72, 0.0)"],
        ]);

        // Warm Amber-Gold bridge along left waist (#FBBC04)
        paintCloud(3.0, 28.0, 29, 26, 0.30, [
          [0.0, "rgba(255, 200, 18, 1.0)"],
          [0.48, "rgba(255, 206, 28, 0.88)"],
          [0.80, "rgba(255, 196, 16, 0.24)"],
          [1.0, "rgba(255, 200, 18, 0.0)"],
        ]);

        // Radiant Sun-Yellow core on the left tip (#FFE432)
        paintCloud(3.0, 33.5, 21, 16, 0.16, [
          [0.0, "rgba(255, 238, 76, 1.0)"],
          [0.56, "rgba(255, 228, 56, 0.92)"],
          [1.0, "rgba(255, 232, 62, 0.0)"],
        ]);

        // Dominant Google Blue sweep reinforcing right half & smooth center blend (#3186FF)
        paintCloud(47.5, 32.5, 31, 28, 0.24, [
          [0.0, "rgba(62, 148, 255, 0.98)"],
          [0.50, "rgba(56, 142, 255, 0.88)"],
          [0.78, "rgba(76, 156, 255, 0.32)"],
          [1.0, "rgba(62, 148, 255, 0.0)"],
        ]);

        // Soft Periwinkle-Azure upper-right rim sheen (#749BFF)
        paintCloud(43.5, 12.5, 21, 14, -0.58, [
          [0.0, "rgba(130, 170, 255, 0.62)"],
          [0.65, "rgba(130, 170, 255, 0.22)"],
          [1.0, "rgba(130, 170, 255, 0.0)"],
        ]);

        g.restore();

        const data = g.getImageData(0, 0, w, h).data;
        const mask = new Uint8Array(w * h);
        const rgbFlat = new Float32Array(w * h * 3);
        for (let i = 0; i < w * h; i++) {
          if (data[i * 4 + 3] > 110) {
            mask[i] = 1;
            rgbFlat[i * 3] = data[i * 4];
            rgbFlat[i * 3 + 1] = data[i * 4 + 1];
            rgbFlat[i * 3 + 2] = data[i * 4 + 2];
          }
        }
        return buildSurfaceFromMask(w, h, mask, rgbFlat, "GEMINI", 1.0, false);
      }

      // 4. Flying Christmas Angel (12 graceful wing-flap frames)
      const ANGEL_FRAMES = 12;
      function buildAngelFrames() {
        const w = 192, h = 176;
        const frames = [];
        const tmpC = document.createElement("canvas");
        tmpC.width = w;
        tmpC.height = h;
        const g = tmpC.getContext("2d");

        for (let fi = 0; fi < ANGEL_FRAMES; fi++) {
          const flap = Math.sin((fi / ANGEL_FRAMES) * Math.PI * 2);
          const wingY = flap * 14;
          g.clearRect(0, 0, w, h);
          const cx = w * 0.5;

          for (const side of [-1, 1]) {
            const wg = g.createLinearGradient(cx, 66, cx + side * 86, 54 - wingY);
            wg.addColorStop(0, "rgb(240, 246, 255)");
            wg.addColorStop(0.55, "rgb(176, 214, 250)");
            wg.addColorStop(1, "rgb(114, 176, 242)");
            g.fillStyle = wg;
            g.beginPath();
            g.moveTo(cx + side * 12, 74);
            g.bezierCurveTo(cx + side * 38, 42 - wingY * 0.85, cx + side * 72, 34 - wingY, cx + side * 88, 52 - wingY * 0.9);
            g.bezierCurveTo(cx + side * 84, 78 - wingY * 0.45, cx + side * 66, 98 - wingY * 0.2, cx + side * 46, 112 - wingY * 0.1);
            g.quadraticCurveTo(cx + side * 26, 108, cx + side * 14, 96);
            g.closePath();
            g.fill();
          }

          const rg = g.createLinearGradient(cx, 72, cx, 162);
          rg.addColorStop(0, "rgb(255, 250, 240)");
          rg.addColorStop(0.55, "rgb(252, 232, 192)");
          rg.addColorStop(1, "rgb(245, 200, 122)");
          g.fillStyle = rg;
          g.beginPath();
          g.moveTo(cx - 14, 72);
          g.lineTo(cx + 14, 72);
          g.bezierCurveTo(cx + 22, 104, cx + 34, 134, cx + 44, 158);
          g.quadraticCurveTo(cx, 168 + flap * 2.5, cx - 44, 158);
          g.bezierCurveTo(cx - 34, 134, cx - 22, 104, cx - 14, 72);
          g.closePath();
          g.fill();

          g.fillStyle = "rgb(255, 246, 228)";
          g.beginPath();
          g.arc(cx, 54, 15, 0, Math.PI * 2);
          g.fill();

          g.strokeStyle = "rgb(255, 212, 74)";
          g.lineWidth = 8.5;
          g.beginPath();
          g.ellipse(cx, 20 - flap * 1.8, 25, 7.5, 0, 0, Math.PI * 2);
          g.stroke();

          const data = g.getImageData(0, 0, w, h).data;
          const mask = new Uint8Array(w * h);
          const rgbFlat = new Float32Array(w * h * 3);
          for (let i = 0; i < w * h; i++) {
            if (data[i * 4 + 3] > 100) {
              mask[i] = 1;
              rgbFlat[i * 3] = data[i * 4];
              rgbFlat[i * 3 + 1] = data[i * 4 + 1];
              rgbFlat[i * 3 + 2] = data[i * 4 + 2];
            }
          }
          frames.push(buildSurfaceFromMask(w, h, mask, rgbFlat, "ANGELNOEL", h / w, false));
        }
        return frames;
      }

      // 5. Full-ASCII Typographic Banner Textures ("NEON & BEYOND" and "JAPAC CLOUD TECHIES")
      function drawTrackedLine(g, text, cx, cy, fontStr, trackingPx, grad, strokeW) {
        g.font = fontStr;
        g.textAlign = "center";
        g.textBaseline = "middle";
        g.lineJoin = "round";
        const widths = Array.from(text).map((ch) => g.measureText(ch).width);
        const totalW = widths.reduce((a, b) => a + b, 0) + trackingPx * Math.max(0, text.length - 1);
        let curX = cx - totalW * 0.5;
        g.fillStyle = grad;
        g.strokeStyle = grad;
        for (let i = 0; i < text.length; i++) {
          const ch = text[i];
          const cw = widths[i];
          const mx = curX + cw * 0.5;
          if (ch !== " ") {
            if (strokeW > 0) {
              g.lineWidth = strokeW;
              g.strokeText(ch, mx, cy);
            }
            g.fillText(ch, mx, cy);
          }
          curX += cw + trackingPx;
        }
      }

      function paintGeminiField(g, w, h) {
        function paintCloud(cx, cy, rx, ry, rotRad, stops) {
          g.save();
          g.translate(cx, cy);
          g.rotate(rotRad);
          g.scale(1, ry / Math.max(1e-4, rx));
          const grad = g.createRadialGradient(0, 0, 0, 0, 0, rx);
          for (let i = 0; i < stops.length; i++) {
            grad.addColorStop(stops[i][0], stops[i][1]);
          }
          g.fillStyle = grad;
          g.beginPath();
          g.arc(0, 0, rx, 0, Math.PI * 2);
          g.fill();
          g.restore();
        }

        // Exact 2025 Gemini 4-color luminous gradient field (Blue foundation + Coral-Red + Sun-Yellow + Emerald + Periwinkle)
        const baseGrad = g.createLinearGradient(w * 0.18, h * 0.72, w * 0.86, h * 0.24);
        baseGrad.addColorStop(0.0, "#348AFF");
        baseGrad.addColorStop(0.55, "#3C92FF");
        baseGrad.addColorStop(1.0, "#62A6FF");
        g.fillStyle = baseGrad;
        g.fillRect(0, 0, w, h);

        // Bottom Emerald Green bloom (#0CCE70)
        paintCloud(w * 0.36, h * 0.92, w * 0.40, h * 0.50, -0.14, [
          [0.0, "rgba(12, 206, 112, 1.0)"],
          [0.48, "rgba(10, 198, 106, 0.96)"],
          [0.76, "rgba(26, 186, 128, 0.38)"],
          [1.0, "rgba(12, 206, 112, 0.0)"],
        ]);

        // Top Coral-Red bloom (#FF4C48)
        paintCloud(w * 0.38, h * 0.06, w * 0.38, h * 0.44, -0.22, [
          [0.0, "rgba(255, 76, 72, 1.0)"],
          [0.50, "rgba(255, 72, 68, 0.96)"],
          [0.78, "rgba(250, 96, 94, 0.34)"],
          [1.0, "rgba(255, 76, 72, 0.0)"],
        ]);

        // Warm Amber-Gold bridge along left waist (#FFC812)
        paintCloud(w * 0.10, h * 0.45, w * 0.34, h * 0.44, 0.20, [
          [0.0, "rgba(255, 200, 18, 1.0)"],
          [0.48, "rgba(255, 206, 28, 0.88)"],
          [0.80, "rgba(255, 196, 16, 0.24)"],
          [1.0, "rgba(255, 200, 18, 0.0)"],
        ]);

        // Radiant Sun-Yellow core on the left edge (#FFEE4C)
        paintCloud(w * 0.08, h * 0.54, w * 0.24, h * 0.30, 0.12, [
          [0.0, "rgba(255, 238, 76, 1.0)"],
          [0.56, "rgba(255, 228, 56, 0.92)"],
          [1.0, "rgba(255, 232, 62, 0.0)"],
        ]);

        // Dominant Google Blue sweep reinforcing right half & smooth center blend (#3E94FF)
        paintCloud(w * 0.76, h * 0.52, w * 0.44, h * 0.52, 0.16, [
          [0.0, "rgba(62, 148, 255, 0.98)"],
          [0.50, "rgba(56, 142, 255, 0.88)"],
          [0.78, "rgba(76, 156, 255, 0.32)"],
          [1.0, "rgba(62, 148, 255, 0.0)"],
        ]);

        // Soft Periwinkle-Azure upper-right rim sheen (#82AAFF)
        paintCloud(w * 0.72, h * 0.18, w * 0.30, h * 0.28, -0.35, [
          [0.0, "rgba(130, 170, 255, 0.62)"],
          [0.65, "rgba(130, 170, 255, 0.22)"],
          [1.0, "rgba(130, 170, 255, 0.0)"],
        ]);
      }

      function buildBannerAsciiTexture(line1, line2, fillWord, paletteStops) {
        const w = 368, h = 172;
        const c = document.createElement("canvas");
        c.width = w;
        c.height = h;
        const g = c.getContext("2d");
        g.clearRect(0, 0, w, h);

        const isGeminiPalette = paletteStops === "gemini";
        let fill1 = "#FFFFFF";
        let fill2 = "#FFFFFF";
        if (!isGeminiPalette) {
          const grad1 = g.createLinearGradient(28, 0, w - 28, 0);
          paletteStops[0].forEach(([pos, col]) => grad1.addColorStop(pos, col));
          fill1 = grad1;
          const grad2 = g.createLinearGradient(16, 0, w - 16, 0);
          paletteStops[1].forEach(([pos, col]) => grad2.addColorStop(pos, col));
          fill2 = grad2;
        }

        drawTrackedLine(g, line1, w * 0.5, 48, "800 72px 'Inter', sans-serif", 7, fill1, 2.0);

        const isLong = line2.length > 10;
        const font2 = isLong ? "800 40px 'Inter', sans-serif" : "800 52px 'Inter', sans-serif";
        const track2 = isLong ? 3.5 : 5.5;
        drawTrackedLine(g, line2, w * 0.5, 124, font2, track2, fill2, 0.6);

        if (isGeminiPalette) {
          g.save();
          g.globalCompositeOperation = "source-atop";
          paintGeminiField(g, w, h);
          g.restore();
        }

        const data = g.getImageData(0, 0, w, h).data;
        const mask = new Uint8Array(w * h);
        const rgbFlat = new Float32Array(w * h * 3);
        for (let i = 0; i < w * h; i++) {
          if (data[i * 4 + 3] > 120) {
            mask[i] = 1;
            rgbFlat[i * 3] = data[i * 4];
            rgbFlat[i * 3 + 1] = data[i * 4 + 1];
            rgbFlat[i * 3 + 2] = data[i * 4 + 2];
          }
        }
        return buildSurfaceFromMask(w, h, mask, rgbFlat, fillWord, h / w, false);
      }

      // 6. Hero Astronomical Rotating 3D Mars (22° obliquity, 100% seamless 360° periodic geography & rotating ASCII globe)
      const MARS_SUN = [-0.70, -0.36, 0.62];
      const MARS_SUN_LEN = Math.hypot(MARS_SUN[0], MARS_SUN[1], MARS_SUN[2]);
      MARS_SUN[0] /= MARS_SUN_LEN;
      MARS_SUN[1] /= MARS_SUN_LEN;
      MARS_SUN[2] /= MARS_SUN_LEN;
      const MARS_OBL_COS = Math.cos(0.384); // ~22° axial tilt
      const MARS_OBL_SIN = Math.sin(0.384);

      function sampleMarsPoint(u, v, t) {
        const R = 0.84;
        const r2 = u * u + v * v;
        if (r2 > R * R) return null;

        const z = Math.sqrt(Math.max(0, R * R - r2));
        const nx = u / R, ny = v / R, nz = z / R;

        // Apply authentic ~22° Martian axial obliquity before evaluating latitude & longitude
        const tx = nx * MARS_OBL_COS + ny * MARS_OBL_SIN;
        const ty = -nx * MARS_OBL_SIN + ny * MARS_OBL_COS;
        const tz = nz;

        const lat = Math.asin(Math.max(-1, Math.min(1, ty)));
        const lon = Math.atan2(tx, tz) - marsSpinAngle;
        const cosLat = Math.cos(lat);

        // 100% periodic 360° seamless Martian geography (Syrtis Major basalt, Tharsis highlands, Valles Marineris, Olympus Mons, Hellas)
        const mare =
          0.52 * Math.sin(lon * 2 + Math.sin(lat * 2) * 0.72) * cosLat +
          0.34 * Math.cos(lon - lat * 1.65) * cosLat +
          0.22 * Math.sin(lon * 3 + lat * 2.15) * cosLat;
        const ridges =
          0.34 * Math.sin(lon * 5 - lat * 4.0) * cosLat +
          0.26 * Math.cos(lon * 4 + lat * 5.6) * cosLat;
        const dLonCanyon = Math.sin((lon - 0.42) * 0.5);
        const canyon =
          Math.exp(-Math.pow((lat + 0.08 - 0.10 * Math.sin(lon * 2)) / 0.085, 2)) *
          Math.exp(-Math.pow(dLonCanyon / 0.28, 2));
        const dOlymp = Math.pow(Math.sin((lon + 1.45) * 0.5) * 2.0, 2) + Math.pow(lat - 0.26, 2);
        const olympus = Math.exp(-dOlymp / 0.075);
        const dHellas = Math.pow(Math.sin((lon - 2.15) * 0.5) * 2.0, 2) + Math.pow(lat + 0.46, 2);
        const hellas = Math.exp(-dHellas / 0.095);

        const albedo = Math.max(
          0,
          Math.min(1, 0.52 + 0.30 * mare + 0.14 * ridges + 0.24 * olympus - 0.52 * canyon - 0.32 * hellas)
        );

        // Rich Martian iron-oxide & basalt editorial palette
        const deepBasalt = [78, 24, 18];
        const rustIron = [198, 68, 36];
        const terracotta = [234, 108, 56];
        const dustyOchre = [254, 186, 124];
        const polarFrost = [240, 246, 255];

        let col;
        if (albedo < 0.38) {
          col = lerpColor(deepBasalt, rustIron, albedo / 0.38);
        } else if (albedo < 0.70) {
          col = lerpColor(rustIron, terracotta, (albedo - 0.38) / 0.32);
        } else {
          col = lerpColor(terracotta, dustyOchre, (albedo - 0.70) / 0.30);
        }

        // Crisp periodic north & south polar ice caps rotating around the tilted axis
        const polar = Math.max(
          0,
          Math.min(1, (Math.abs(lat) - 1.16 + 0.055 * Math.sin(lon * 4) + 0.03 * Math.cos(lon * 6)) / 0.12)
        );
        if (polar > 0) col = lerpColor(col, polarFrost, polar);

        // High-contrast 3D solar terminator + warm atmospheric limb scatter & backlit eclipse corona rim
        const ndotl = Math.max(0, nx * MARS_SUN[0] + ny * MARS_SUN[1] + nz * MARS_SUN[2]);
        const term = Math.pow(ndotl, 0.76);
        const limb = Math.pow(Math.max(0, 1 - nz), 2.75) * (0.14 + 0.86 * ndotl);
        const backAlign = Math.max(0, nx * MARS_SUN[0] + ny * MARS_SUN[1] + 0.45);
        const backEclipse = Math.pow(Math.max(0, 1 - nz), 3.1) * Math.max(0, -MARS_SUN[2]) * (0.35 + 0.65 * backAlign);
        const rimGlow = limb + backEclipse * 1.15;

        const shade = 0.09 + 1.08 * term;
        const lr = Math.min(255, col[0] * shade + 255 * 0.56 * rimGlow);
        const lg = Math.min(255, col[1] * shade + 162 * 0.56 * rimGlow);
        const lb = Math.min(255, col[2] * shade + 96 * 0.56 * rimGlow);

        // Seamless 3D spherical lat/lon rotating ASCII typography ("MARS" marches around the rotating globe!)
        const lonIdx = Math.floor(((lon / (Math.PI * 2)) + 1000.0) * 56.0);
        const latIdx = Math.floor(((lat / Math.PI) + 10.0) * 28.0);
        const effLit = Math.max(ndotl, backEclipse * 0.72);
        let chOverride;
        if (effLit < 0.035) chOverride = "·";
        else if (effLit < 0.11) chOverride = ":";
        else if (effLit < 0.21) chOverride = "+";
        else if (polar > 0.55 && ndotl >= 0.14) chOverride = "*";
        else chOverride = "MARS"[modPos(lonIdx + latIdx * 2, 4)];

        const alpha = effLit < 0.035 ? 0.34 : effLit < 0.11 ? 0.64 : 0.98;
        return { r: lr, g: lg, b: lb, alpha, chOverride, prelit: true };
      }

      // Unified ASCII sampler for ALL 7 modes
      function samplePattern(key, u, v, t, angelFrameIdx) {
        if (key === "mars") {
          if (u < -1 || u > 1 || v < -1 || v > 1) return null;
          return sampleMarsPoint(u, v, t);
        }

        const tex = key === "angel" ? angelFrames[angelFrameIdx] : textures[key];
        if (!tex) return null;

        const invScale = key === "gemini" ? 0.96 : 1.0;
        const su = u * invScale;
        const sv = v * invScale;
        if (su < -1 || su > 1 || sv < -1 || sv > 1) return null;

        const ix = Math.round((su * 0.5 + 0.5) * (tex.w - 1));
        const iy = Math.round((sv * 0.5 + 0.5) * (tex.h - 1));
        if (ix < 0 || ix >= tex.w || iy < 0 || iy >= tex.h) return null;
        const idx = iy * tex.w + ix;
        if (!tex.mask[idx]) return null;

        return {
          nx: tex.nx[idx],
          ny: tex.ny[idx],
          nz: tex.nz[idx],
          edge: tex.edge[idx],
          r: tex.rgb[idx * 3],
          g: tex.rgb[idx * 3 + 1],
          b: tex.rgb[idx * 3 + 2],
          alpha: 0.96,
          prelit: false,
        };
      }

      // Whisper-quiet winter snow drifting along the exact same unified diagonal vector (+22° upward-right)
      const snowRand = mulberry32(1225);
      const snowflakes = Array.from({ length: 110 }, (_, i) => {
        const depth = 0.3 + snowRand() * 0.7;
        const speed = WIND_SPEED_PX * (0.48 + 0.44 * depth);
        return {
          x: snowRand() * 1600,
          y: snowRand() * 1000,
          vxBase: speed * DIAG_X,
          vyBase: speed * DIAG_Y,
          phase: snowRand() * Math.PI * 2,
          depth,
          ch: i % 14 === 0 ? "*" : i % 6 === 0 ? "+" : "·",
          tint: i % 5 === 0 ? WINTER_TINTS[i % WINTER_TINTS.length] : null,
        };
      });

      // Dedicated deep-space ASCII starfield for Mars mode (stationary cosmic parallax, zero water/snow drift)
      const starRand = mulberry32(4049);
      const STAR_TINTS = [
        [236, 242, 255],
        [194, 218, 255],
        [255, 232, 198],
      ];
      const marsStars = Array.from({ length: 165 }, (_, i) => {
        const depth = 0.15 + starRand() * 0.85;
        return {
          nx: starRand(),
          ny: starRand(),
          depth,
          phase: starRand() * Math.PI * 2,
          speed: 0.55 + starRand() * 1.15,
          ch: i % 19 === 0 ? "*" : i % 7 === 0 ? "+" : i % 3 === 0 ? "·" : ".",
          tint: STAR_TINTS[i % STAR_TINTS.length],
        };
      });

      const LOGO_WORDS = {
        cloud: "GOOGLECLOUD",
        google: "GOOGLE",
        gemini: "GEMINI",
        mars: "MARS",
        angel: "ANGELNOEL",
        neon: "NEONANDBEYOND",
        japac: "JAPACCLOUDTECHIES",
      };

      const angelFrames = buildAngelFrames();
      const textures = {
        cloud: null,
        google: buildGoogleTexture(),
        gemini: buildGeminiTexture(),
        mars: { aspect: 1.0 },
        angel: { aspect: 176 / 192 },
        neon: null,
        japac: null,
      };

      const MODE_ORDER = ["cloud", "google", "gemini", "mars", "angel", "neon", "japac"];
      const ALLOWED_MODES = new Set(MODE_ORDER);
      const urlParams = new URLSearchParams(window.location.search);
      const initParam = (urlParams.get("logo") || "").trim().toLowerCase();
      let activeLogo = ALLOWED_MODES.has(initParam) ? initParam : "cloud";
      const demoRipple = urlParams.get("ripple") === "1";
      const AUTO_ROTATE_SEC = 10.0;
      const MARS_ROTATE_SEC = 20.0;
      const FADE_OUT_SEC = 2.4;
      const FADE_HOLD_SEC = 0.35;
      const FADE_IN_SEC = 2.6;
      const MANUAL_FADE_IN_SEC = 0.85;
      const autoRotateEnabled = urlParams.get("auto") !== "0";
      let autoRotateElapsed = 0;
      // Ultra-slow cinema fade transition state (2.4s fade-out -> 0.35s dark breath -> 2.6s fade-in)
      let fadePhase = "idle"; // "idle" | "out" | "hold" | "in"
      let fadeT = 0;
      let fadeInDur = FADE_IN_SEC;
      let pendingNextLogo = null;
      const getModeDuration = (key) => (key === "mars" ? MARS_ROTATE_SEC : AUTO_ROTATE_SEC);

      let simTime = 0;
      let lastTs = performance.now();

      // Exact hit-test against visible foreground logos (including wrapped copies)
      function hitTestForegroundLogo(clientX, clientY) {
        const angelFrame = Math.floor(modPos(simTime * 8.0, ANGEL_FRAMES));
        const tex = activeLogo === "angel" ? angelFrames[angelFrame] : textures[activeLogo];
        const logoAspect = tex ? tex.aspect : 1.0;
        const wrapX = OBJ_DRAW_W * 0.65 + 28;
        const wrapY = OBJ_DRAW_W * 0.65 + 28;
        const fgParX = -ptrSmoothX * 14.0;
        const fgParY = -ptrSmoothY * 10.0;

        const isHeroMars = activeLogo === "mars";
        for (let i = bodies.length - 1; i >= 0; i--) {
          const b = bodies[i];
          const scale = b.bobScale || 1.0;
          const sinkPx = (b.sink || 0) * 125.0;
          const camDHit = isHeroMars ? 720.0 : 430.0;
          const perspC = camDHit / Math.max(175.0, camDHit + sinkPx);
          const halfW = OBJ_DRAW_W * scale * perspC * 0.5;
          const halfH = halfW * logoAspect;
          const bound = Math.hypot(halfW, halfH) + 12;
          const cosA = Math.cos(b.angle);
          const sinA = Math.sin(b.angle);

          const bx = b.x + fgParX;
          const by = b.y + fgParY;
          const xs = [[bx, 0]];
          const ys = [[by, 0]];
          if (!isHeroMars) {
            if (bx < wrapX) xs.push([bx + SPAN_X, SPAN_X]);
            if (bx > viewW - wrapX) xs.push([bx - SPAN_X, -SPAN_X]);
            if (by < wrapY) ys.push([by + SPAN_Y, SPAN_Y]);
            if (by > viewH - wrapY) ys.push([by - SPAN_Y, -SPAN_Y]);
          }

          for (let xi = 0; xi < xs.length; xi++) {
            for (let yi = 0; yi < ys.length; yi++) {
              const cx = xs[xi][0];
              const cy = ys[yi][0];
              const dx = clientX - cx;
              const dy = clientY - cy;
              if (dx < -bound || dx > bound || dy < -bound || dy > bound) continue;
              const lx = dx * cosA + dy * sinA;
              const ly = -dx * sinA + dy * cosA;
              const u = lx / Math.max(1, halfW);
              const v = ly / Math.max(1, halfH);
              if (isInsideLogoSilhouette(activeLogo, u, v, angelFrame)) {
                return {
                  body: b,
                  u: Math.max(-1, Math.min(1, u)),
                  v: Math.max(-1, Math.min(1, v)),
                  wrapDx: xs[xi][1],
                  wrapDy: ys[yi][1],
                };
              }
            }
          }
        }
        return null;
      }

      function handlePointerRelease() {
        if (!pointerDown) return;
        const held = pressHold;
        const heldDuration = simTime - pressStartTime;
        const body = pressedBody;
        const rx = pressX;
        const ry = pressY;
        const u = pressU;
        const v = pressV;

        pointerDown = false;
        pressedBody = null;
        pressHold = 0;

        // Mars is deep space: no water rebound splash on pointer release
        if (activeLogo === "mars") return;

        if (body) {
          // Smooth buoyant rise back up to the surface + fresh release wave radiating outward!
          const popPower = 0.55 + held * 1.05;
          body.vSink -= 3.3 * popPower;
          body.vTiltY -= u * 1.9 * popPower;
          body.vTiltX -= v * 1.9 * popPower;
          const fgParX = -ptrSmoothX * 14.0;
          const fgParY = -ptrSmoothY * 10.0;
          const splashX = body.x + fgParX + pressWrapDx + u * OBJ_DRAW_W * 0.22;
          const splashY = body.y + fgParY + pressWrapDy + v * OBJ_DRAW_W * 0.22;
          releaseWaterRebound(
            Math.max(0, Math.min(viewW, splashX)),
            Math.max(0, Math.min(viewH, splashY)),
            0.80 + held * 0.95,
            3.1 + held * 1.1
          );
        } else if (heldDuration >= 0.13 || held > 0.25) {
          // Releasing a pressed water depression springs the surface upward into a fresh 360° wave!
          releaseWaterRebound(rx, ry, 0.78 + held * 0.95, 3.0 + held * 1.1);
        }
      }

      canvas.addEventListener("pointerdown", (e) => {
        pointerDown = true;
        pressStartTime = simTime;
        pressHold = 0;
        pressX = e.clientX;
        pressY = e.clientY;
        lastDragX = e.clientX;
        lastDragY = e.clientY;

        const hit = hitTestForegroundLogo(e.clientX, e.clientY);
        if (activeLogo === "mars") {
          // Deep-space Mars: click open space to launch a shooting star (or drag to revolve Sun); drag on Mars to turn slowly
          pressedBody = hit ? hit.body : null;
          if (!hit) {
            spawnMarsMeteor(e.clientX, e.clientY, false);
          }
          return;
        }

        if (hit) {
          pressedBody = hit.body;
          pressU = hit.u;
          pressV = hit.v;
          pressWrapDx = hit.wrapDx;
          pressWrapDy = hit.wrapDy;
          // Immediate tactile push-down impulse + entry displacement ripple around the pressed side
          hit.body.vSink += 2.2;
          hit.body.vTiltY += hit.u * 1.5;
          hit.body.vTiltX += hit.v * 1.5;
          injectWaterDrop(e.clientX, e.clientY, 0.95, 3.1);
        } else {
          pressedBody = null;
          injectWaterDrop(e.clientX, e.clientY, 1.0, 2.8);
        }
      });

      window.addEventListener("pointermove", (e) => {
        ptrTargetX = (e.clientX / Math.max(1, viewW)) * 2 - 1;
        ptrTargetY = (e.clientY / Math.max(1, viewH)) * 2 - 1;
        if (!pointerDown) return;

        pressX = e.clientX;
        pressY = e.clientY;

        if (activeLogo === "mars") {
          const dragDx = e.clientX - lastDragX;
          lastDragX = e.clientX;
          lastDragY = e.clientY;
          if (Math.abs(dragDx) > 0.1) {
            if (pressedBody) {
              // Gentle capped spin when dragging directly on Mars (never frantically fast)
              const dTheta = dragDx * 0.0042;
              marsSpinAngle += dTheta;
              marsSpinVel = Math.max(-0.85, Math.min(0.85, dTheta * 24.0));
            } else {
              // Dragging in deep space revolves the orbiting Sun smoothly to shift the lit hemisphere
              marsSunAngle += dragDx * 0.0052;
              updateMarsSunVector();
            }
          }
          return;
        }

        if (pressedBody) {
          // Track which side of the held logo the finger is pressing so tilt follows smoothly
          const fgParX = -ptrSmoothX * 14.0;
          const fgParY = -ptrSmoothY * 10.0;
          const cx = pressedBody.x + fgParX + pressWrapDx;
          const cy = pressedBody.y + fgParY + pressWrapDy;
          const dx = e.clientX - cx;
          const dy = e.clientY - cy;
          const cosA = Math.cos(pressedBody.angle);
          const sinA = Math.sin(pressedBody.angle);
          const lx = dx * cosA + dy * sinA;
          const ly = -dx * sinA + dy * cosA;
          const texH = activeLogo === "angel" ? angelFrames[0] : textures[activeLogo];
          const halfW = OBJ_DRAW_W * 0.5;
          const halfH = halfW * (texH ? texH.aspect : 1.0);
          const u = lx / Math.max(1, halfW);
          const v = ly / Math.max(1, halfH);
          if (Math.hypot(u, v) > 1.35) {
            // Finger slid off the logo into open water: pop the logo cleanly and keep pressing water
            const released = pressedBody;
            pressedBody = null;
            released.vSink -= 2.7 * (0.5 + pressHold);
            releaseWaterRebound(cx, cy, 0.8 + pressHold * 0.9, 3.2);
          } else {
            pressU = Math.max(-1, Math.min(1, u));
            pressV = Math.max(-1, Math.min(1, v));
          }
          return;
        }

        const d = Math.hypot(e.clientX - lastDragX, e.clientY - lastDragY);
        if (d > 26) {
          lastDragX = e.clientX;
          lastDragY = e.clientY;
          injectWaterDrop(e.clientX, e.clientY, 0.38, 2.0);
        }
      });

      window.addEventListener("pointerup", handlePointerRelease);
      window.addEventListener("pointercancel", handlePointerRelease);
      document.addEventListener("mouseleave", () => {
        handlePointerRelease();
        ptrTargetX = 0;
        ptrTargetY = 0;
      });

      const logoButtons = Array.from(document.querySelectorAll(".logo-btn"));
      function selectLogo(key, fromAuto) {
        if (!ALLOWED_MODES.has(key)) return;
        pointerDown = false;
        pressedBody = null;
        pressHold = 0;
        autoRotateElapsed = 0;
        if (!fromAuto && key === activeLogo) {
          fadePhase = "idle";
          fadeT = 0;
          pendingNextLogo = null;
          return;
        }
        if (!fromAuto) {
          fadePhase = "in";
          fadeT = 0;
          fadeInDur = MANUAL_FADE_IN_SEC;
          pendingNextLogo = null;
        }
        const wasBanner = activeLogo === "neon" || activeLogo === "japac";
        const isBanner = key === "neon" || key === "japac";
        const wasMars = activeLogo === "mars";
        const isMars = key === "mars";
        activeLogo = key;
        if (isMars) {
          hPrev.fill(0);
          hCurr.fill(0);
          surfaceDrops.length = 0;
          marsMeteors.length = 0;
          nextAmbientMeteorAt = simTime + 5.0;
          marsSpinVel = MARS_BASE_SPIN;
          updateMarsSunVector();
        } else if (wasMars) {
          marsMeteors.length = 0;
        }
        if (wasBanner !== isBanner || wasMars !== isMars) rebuildBodies();
        logoButtons.forEach((btn) => {
          const isActive = btn.dataset.logo === key;
          btn.setAttribute("aria-pressed", String(isActive));
          if (isActive && typeof btn.scrollIntoView === "function") {
            btn.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
          }
        });
      }

      logoButtons.forEach((btn) => {
        btn.setAttribute("aria-pressed", String(btn.dataset.logo === activeLogo));
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          selectLogo(btn.dataset.logo, false);
        });
      });

      window.addEventListener("resize", updateLayoutMetrics);

      const KEY_LIGHT = [-0.38, -0.44, 0.81];
      const HALF_VEC = [-0.22, -0.27, 0.93];

      // Object-locked local ASCII grid renderer: characters stay 100% bound to (lc, lr)
      // and glide at smooth sub-pixel coordinates — ZERO letter swapping or jitter!
      function drawBuoyantBody(body, drawX, drawY, t, angelFrame, drawW, cellW, cellH, layerAlpha, isFarLayer) {
        const tex = activeLogo === "angel" ? angelFrames[angelFrame] : textures[activeLogo];
        if (!tex) return;

        const aspect = tex.aspect;
        const scale = body.bobScale || 1.0;
        const effW = drawW * scale;
        const halfW = effW * 0.5;
        const halfH = halfW * aspect;
        const bound = Math.hypot(halfW, halfH) + 38;

        // Fast viewport cull before iterating local cells
        if (
          drawX + bound < 0 ||
          drawX - bound > viewW ||
          drawY + bound < 0 ||
          drawY - bound > viewH
        ) {
          return;
        }

        const stepW = cellW * scale;
        const stepH = cellH * scale;
        const maxC = Math.ceil(halfW / stepW);
        const maxR = Math.ceil(halfH / stepH);
        const cosA = Math.cos(body.angle);
        const sinA = Math.sin(body.angle);
        const word = LOGO_WORDS[activeLogo];

        // Rigid 3D plane tilt & submersion perspective when pressed into the water (zero jelly distortion!)
        const sinkPx = (body.sink || 0) * 128.0;
        const tX = body.tiltX || 0;
        const tY = body.tiltY || 0;
        const has3DTilt = Math.abs(sinkPx) > 0.25 || Math.abs(tX) > 0.004 || Math.abs(tY) > 0.004;
        const cosTX = has3DTilt ? Math.cos(tX) : 1.0;
        const sinTX = has3DTilt ? Math.sin(tX) : 0.0;
        const cosTY = has3DTilt ? Math.cos(tY) : 1.0;
        const sinTY = has3DTilt ? Math.sin(tY) : 0.0;
        const camD = activeLogo === "mars" ? 720.0 : 430.0;

        for (let lr = -maxR; lr <= maxR; lr++) {
          const ly = lr * stepH;
          const v = ly / halfH;
          if (v < -1.02 || v > 1.02) continue;

          for (let lc = -maxC; lc <= maxC; lc++) {
            const lx = lc * stepW;
            const u = lx / halfW;
            if (u < -1.02 || u > 1.02) continue;

            // Rigid 3D tilted plane projection: pressed side plunges deeper in perspective while keeping exact geometry
            let plx = lx;
            let ply = ly;
            let zDepth = 0;
            if (has3DTilt) {
              zDepth = sinkPx + lx * sinTY + ly * sinTX;
              const persp = camD / Math.max(175.0, camD + zDepth);
              plx = lx * cosTY * persp;
              ply = ly * cosTX * persp;
            }

            const sx = drawX + plx * cosA - ply * sinA;
            const sy = drawY + plx * sinA + ply * cosA;
            if (sx < -24 || sx > viewW + 24 || sy < -24 || sy > viewH + 24) {
              continue;
            }

            const hit = samplePattern(activeLogo, u, v, t, angelFrame);
            if (!hit) continue;

            let lrCol, lgCol, lbCol;
            let alpha = hit.alpha * layerAlpha;
            let ch = hit.chOverride;

            if (hit.prelit) {
              lrCol = hit.r;
              lgCol = hit.g;
              lbCol = hit.b;
            } else {
              // Rotate intact surface normal with the rigid body's rocking angle so light glides naturally as it tilts
              const rnx = hit.nx * cosA - hit.ny * sinA;
              const rny = hit.nx * sinA + hit.ny * cosA;
              const rnz = Math.max(0.14, hit.nz);
              const nlen = Math.hypot(rnx, rny, rnz);
              const unx = rnx / nlen, uny = rny / nlen, unz = rnz / nlen;

              const ndotl = Math.max(0, unx * KEY_LIGHT[0] + uny * KEY_LIGHT[1] + unz * KEY_LIGHT[2]);
              const spec = Math.pow(Math.max(0, unx * HALF_VEC[0] + uny * HALF_VEC[1] + unz * HALF_VEC[2]), 12);
              const fres = Math.pow(Math.max(0, 1 - unz), 2.2);

              const shade = 0.58 + 0.52 * ndotl;
              lrCol = Math.min(255, hit.r * shade + 255 * 0.28 * spec + 205 * 0.18 * fres);
              lgCol = Math.min(255, hit.g * shade + 248 * 0.28 * spec + 228 * 0.18 * fres);
              lbCol = Math.min(255, hit.b * shade + 240 * 0.28 * spec + 255 * 0.18 * fres);

              // Subtle sculpted edge softening for airy translucent glass edges
              if (hit.edge !== undefined && hit.edge < 0.12) {
                alpha *= 0.68 + (hit.edge / 0.12) * 0.32;
              }
            }

            // Underwater optical depth dimming & cool nocturnal sapphire absorption on the submerged side
            if (has3DTilt) {
              if (zDepth > 4.0) {
                const subT = Math.min(1.0, zDepth / 185.0);
                const dim = 1.0 - subT * 0.52;
                const tintW = subT * 0.42;
                lrCol = lrCol * dim * (1 - tintW) + 14 * tintW;
                lgCol = lgCol * dim * (1 - tintW) + 34 * tintW;
                lbCol = lbCol * dim * (1 - tintW) + 74 * tintW;
                alpha *= 1.0 - subT * 0.34;
              } else if (zDepth < -4.0) {
                // Crisp subtle crest sheen when breaching slightly upward on buoyant release
                const liftT = Math.min(1.0, -zDepth / 95.0);
                lrCol = Math.min(255, lrCol * (1 + liftT * 0.12) + 12 * liftT);
                lgCol = Math.min(255, lgCol * (1 + liftT * 0.12) + 14 * liftT);
                lbCol = Math.min(255, lbCol * (1 + liftT * 0.12) + 18 * liftT);
              }
            }

            if (isFarLayer) {
              // Subtle cool atmospheric depth mist on far-background parallax silhouettes
              lrCol = lrCol * 0.78 + 26;
              lgCol = lgCol * 0.84 + 34;
              lbCol = lbCol * 0.94 + 48;
            }

            if (!ch) {
              ch = word[modPos(lc + lr * 3, word.length)];
            }
            octx.fillStyle = `rgba(${lrCol | 0}, ${lgCol | 0}, ${lbCol | 0}, ${alpha.toFixed(3)})`;
            octx.fillText(ch, sx, sy);
          }
        }
      }

      // Exact 1:1 logo glyph footprint hit-test (matches samplePattern with ZERO inflated border/moat!)
      function isInsideLogoSilhouette(key, u, v, angelFrame) {
        if (key === "mars") {
          return u * u + v * v <= 0.84 * 0.84;
        }
        const tex = key === "angel" ? angelFrames[angelFrame] : textures[key];
        const m = tex && (tex.solidMask || tex.mask);
        if (!m) return false;
        const invScale = key === "gemini" ? 0.96 : 1.0;
        const su = u * invScale;
        const sv = v * invScale;
        if (su < -1 || su > 1 || sv < -1 || sv > 1) return false;
        const ix = Math.round((su * 0.5 + 0.5) * (tex.w - 1));
        const iy = Math.round((sv * 0.5 + 0.5) * (tex.h - 1));
        if (ix < 0 || ix >= tex.w || iy < 0 || iy >= tex.h) return false;
        return Boolean(m[iy * tex.w + ix]);
      }

      // 100% Pure Monospace ASCII Water Waves driven directly by the real 2D open-ocean PDE heightfield
      // Matches the exact 8x10 JetBrains Mono grid of the logos, flows right up to the exact logo characters!
      function drawAsciiWaterWaves(t, angelFrame, fgParX, fgParY) {
        const LIFE = 6.5;
        while (surfaceDrops.length > 0 && t - surfaceDrops[0].t0 > LIFE) {
          surfaceDrops.shift();
        }
        if (surfaceDrops.length === 0) return;

        // 1. Find active PDE bounding box within the visible interior fluid grid
        const xStart = F_PAD;
        const xEnd = F_PAD + FW_VIS - 1;
        const yStart = F_PAD;
        const yEnd = F_PAD + FH_VIS - 1;
        let fMinX = xEnd + 1, fMaxX = xStart - 1, fMinY = yEnd + 1, fMaxY = yStart - 1;
        for (let y = yStart; y <= yEnd; y++) {
          const y0 = y * FW;
          for (let x = xStart; x <= xEnd; x++) {
            const idx = y0 + x;
            const v = hCurr[idx];
            const vp = hPrev[idx];
            if (v > 0.014 || v < -0.014 || vp > 0.014 || vp < -0.014) {
              if (x < fMinX) fMinX = x;
              if (x > fMaxX) fMaxX = x;
              if (y < fMinY) fMinY = y;
              if (y > fMaxY) fMaxY = y;
            }
          }
        }
        if (fMaxX < fMinX) return;

        // Expand slightly for gradient tails and map to screen ASCII grid
        const pxMinX = Math.max(0, ((fMinX - F_PAD - 2) / (FW_VIS - 1)) * viewW);
        const pxMaxX = Math.min(viewW, ((fMaxX - F_PAD + 2) / (FW_VIS - 1)) * viewW);
        const pxMinY = Math.max(0, ((fMinY - F_PAD - 2) / (FH_VIS - 1)) * viewH);
        const pxMaxY = Math.min(viewH, ((fMaxY - F_PAD + 2) / (FH_VIS - 1)) * viewH);

        // 2. Collect visible foreground rigid logo transforms for exact silhouette occlusion
        const tex = activeLogo === "angel" ? angelFrames[angelFrame] : textures[activeLogo];
        const logoAspect = tex ? tex.aspect : 1.0;
        const wrapX = OBJ_DRAW_W * 0.65 + 28;
        const wrapY = OBJ_DRAW_W * 0.65 + 28;
        const fgOccluders = [];

        const isHeroMarsOcc = activeLogo === "mars";
        for (let i = 0; i < bodies.length; i++) {
          const b = bodies[i];
          const scale = b.bobScale || 1.0;
          const sinkPx = (b.sink || 0) * 128.0;
          const camDOcc = isHeroMarsOcc ? 720.0 : 430.0;
          const perspC = camDOcc / Math.max(175.0, camDOcc + sinkPx);
          const halfW = OBJ_DRAW_W * scale * perspC * Math.cos(b.tiltY || 0) * 0.5;
          const halfH = OBJ_DRAW_W * scale * perspC * Math.cos(b.tiltX || 0) * logoAspect * 0.5;
          const bound = Math.hypot(halfW, halfH) + 14;
          const cosA = Math.cos(b.angle);
          const sinA = Math.sin(b.angle);

          const bx = b.x + fgParX;
          const by = b.y + fgParY;
          const xs = [bx];
          const ys = [by];
          if (!isHeroMarsOcc) {
            if (bx < wrapX) xs.push(bx + SPAN_X);
            if (bx > viewW - wrapX) xs.push(bx - SPAN_X);
            if (by < wrapY) ys.push(by + SPAN_Y);
            if (by > viewH - wrapY) ys.push(by - SPAN_Y);
          }

          for (let xi = 0; xi < xs.length; xi++) {
            for (let yi = 0; yi < ys.length; yi++) {
              const cx = xs[xi];
              const cy = ys[yi];
              if (cx + bound < pxMinX || cx - bound > pxMaxX || cy + bound < pxMinY || cy - bound > pxMaxY) {
                continue;
              }
              fgOccluders.push({ cx, cy, halfW, halfH, bound, cosA, sinA });
            }
          }
        }

        // 3. Render pure monospace ASCII wave glyphs on the exact CELL_W x CELL_H (8x10) typography grid
        const startC = Math.max(0, Math.floor(pxMinX / CELL_W));
        const endC = Math.min(Math.ceil(viewW / CELL_W), Math.ceil(pxMaxX / CELL_W));
        const startR = Math.max(0, Math.floor(pxMinY / CELL_H));
        const endR = Math.min(Math.ceil(viewH / CELL_H), Math.ceil(pxMaxY / CELL_H));
        const baseSpec = Math.pow(0.924, 18);

        octx.save();
        octx.font = "600 8.8px 'JetBrains Mono', monospace";
        octx.textAlign = "center";
        octx.textBaseline = "middle";

        for (let r = startR; r <= endR; r++) {
          const gy = (r + 0.5) * CELL_H;
          for (let c = startC; c <= endC; c++) {
            const gx = (c + 0.5) * CELL_W;
            const pde = sampleFluidPDE(gx, gy);
            const slopeMag = Math.hypot(pde.gx, pde.gy);
            const energy = slopeMag * 1.45 + Math.abs(pde.h) * 0.48;
            if (energy < 0.030) continue;

            // 3D directional moonlight shading from the real PDE slope
            const nx = -Math.tanh(pde.gx * 2.1) * 1.55;
            const ny = -Math.tanh(pde.gy * 2.1) * 1.55;
            const invLen = 1 / Math.hypot(nx, ny, 1.0);
            const unx = nx * invLen;
            const uny = ny * invLen;
            const unz = invLen;

            const lit = unx * -0.48 + uny * -0.52 + unz * 0.71;
            const deltaLit = lit - 0.71;
            const ndoth = Math.max(0, unx * -0.26 + uny * -0.28 + unz * 0.924);
            const spec = Math.max(0, Math.pow(ndoth, 18) - baseSpec);

            // Balanced 360° expanding ASCII wave ring with directional upper-left moonlight crest lift
            const directional = Math.max(0, deltaLit * 2.2) + spec * 2.1;
            const omniCrest = Math.max(0, Math.abs(pde.h) * 0.52 + slopeMag * 0.85);
            const intensity = directional * 0.50 + omniCrest * 0.58;
            if (intensity < 0.060) continue;

            // Exact silhouette occlusion: never draw ASCII water wave over or inside foreground rigid logos
            let occluded = false;
            for (let k = 0; k < fgOccluders.length; k++) {
              const oc = fgOccluders[k];
              const dx = gx - oc.cx;
              const dy = gy - oc.cy;
              if (dx < -oc.bound || dx > oc.bound || dy < -oc.bound || dy > oc.bound) continue;
              const lx = dx * oc.cosA + dy * oc.sinA;
              const ly = -dx * oc.sinA + dy * oc.cosA;
              const u = lx / oc.halfW;
              const v = ly / oc.halfH;
              if (u >= -1.04 && u <= 1.04 && v >= -1.04 && v <= 1.04) {
                if (isInsideLogoSilhouette(activeLogo, u, v, angelFrame)) {
                  occluded = true;
                  break;
                }
              }
            }
            if (occluded) continue;

            // Pure classic ASCII wave luminance ramp: '·' -> ':' -> '~' -> '≈'
            let ch;
            let cr, cg, cb;
            if (intensity > 0.54) {
              ch = "≈";
              cr = 186; cg = 220; cb = 255;
            } else if (intensity > 0.31) {
              ch = "~";
              cr = 148; cg = 198; cb = 254;
            } else if (intensity > 0.165) {
              ch = ":";
              cr = 112; cg = 166; cb = 240;
            } else {
              ch = "·";
              cr = 82; cg = 134; cb = 212;
            }

            const alpha = Math.min(0.48, Math.pow(Math.min(1, (intensity - 0.055) * 1.45), 1.15) * 0.48);
            if (alpha < 0.03) continue;

            octx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${alpha.toFixed(3)})`;
            octx.fillText(ch, gx, gy);
          }
        }

        octx.restore();
      }

      // Pure monospace ASCII shooting stars for Mars deep-space mode (cleanly occluded behind Mars)
      function stepAndDrawMarsMeteors(dt, t, marsCx, marsCy, marsR) {
        if (t >= nextAmbientMeteorAt) {
          const sx = (0.08 + Math.random() * 0.84) * viewW;
          const sy = (0.06 + Math.random() * 0.42) * viewH;
          spawnMarsMeteor(sx, sy, true);
          nextAmbientMeteorAt = t + 7.5 + Math.random() * 5.0;
        }
        if (marsMeteors.length === 0) return;

        const occR2 = (marsR + 2) * (marsR + 2);
        octx.save();
        octx.font = "600 9.6px 'JetBrains Mono', monospace";
        octx.textAlign = "center";
        octx.textBaseline = "middle";

        for (let i = marsMeteors.length - 1; i >= 0; i--) {
          const m = marsMeteors[i];
          m.age += dt;
          if (m.age >= m.life) {
            marsMeteors.splice(i, 1);
            continue;
          }
          m.x += m.vx * dt;
          m.y += m.vy * dt;

          const p = m.age / m.life;
          const env = p < 0.10 ? (p / 0.10) : Math.pow(1.0 - (p - 0.10) / 0.90, 1.35);
          const headAlpha = m.peakAlpha * env;
          if (headAlpha < 0.03) continue;

          const curLen = m.tailLen * Math.min(1.0, p * 4.5 + 0.30);
          const steps = Math.max(12, Math.ceil(curLen / 7.0));
          const slashCh = m.dirX >= 0 ? "\\" : "/";
          const perpX = -m.dirY;
          const perpY = m.dirX;
          let prevKey = -1;

          for (let s = 0; s <= steps; s++) {
            const u = s / steps; // 0 = bright head, 1 = faint tail ember
            const dist = u * curLen;
            const scatter = u > 0.52 ? Math.sin(m.seed + s * 2.9) * (u - 0.52) * 5.0 : 0;
            const rawX = m.x - m.dirX * dist + perpX * scatter;
            const rawY = m.y - m.dirY * dist + perpY * scatter;

            // Snap cleanly onto the exact 8x10 monospace ASCII grid
            const col = Math.floor(rawX / CELL_W);
            const row = Math.floor(rawY / CELL_H);
            const cellKey = row * 4096 + col;
            if (cellKey === prevKey) continue;
            prevKey = cellKey;

            const gx = (col + 0.5) * CELL_W;
            const gy = (row + 0.5) * CELL_H;
            if (gx < -16 || gx > viewW + 16 || gy < -16 || gy > viewH + 16) continue;

            const dx = gx - marsCx;
            const dy = gy - marsCy;
            if (dx * dx + dy * dy < occR2) continue;

            const falloff = Math.pow(1.0 - u, 1.45);
            const a = headAlpha * falloff;
            if (a < 0.04) continue;

            let ch;
            let cr, cg, cb;
            if (s === 0) {
              ch = p < 0.65 ? "*" : "+";
              cr = 255; cg = 253; cb = 242;
            } else if (u < 0.24) {
              ch = "+";
              cr = Math.round(255 * 0.62 + m.tint[0] * 0.38);
              cg = Math.round(252 * 0.62 + m.tint[1] * 0.38);
              cb = Math.round(244 * 0.62 + m.tint[2] * 0.38);
            } else if (u < 0.62) {
              ch = slashCh;
              cr = m.tint[0]; cg = m.tint[1]; cb = m.tint[2];
            } else {
              ch = u < 0.82 ? ":" : "·";
              cr = m.tint[0]; cg = m.tint[1]; cb = m.tint[2];
            }

            octx.fillStyle = `rgba(${cr}, ${cg}, ${cb}, ${a.toFixed(3)})`;
            octx.fillText(ch, gx, gy);
          }
        }
        octx.restore();
      }

      // Distant pure monospace ASCII Sun at infinity (visible only in camera forward hemisphere, always behind Mars)
      function drawDistantAsciiSun(sunX, sunY, sunVis, marsCx, marsCy, marsR, t) {
        if (sunVis <= 0.01) return;
        const rHalo = 44.0;
        if (sunX + rHalo < -10 || sunX - rHalo > viewW + 10 || sunY + rHalo < -10 || sunY - rHalo > viewH + 10) {
          return;
        }
        const eclipseOccR2 = (marsR - 1.5) * (marsR - 1.5);
        const startC = Math.max(0, Math.floor((sunX - rHalo - CELL_W) / CELL_W));
        const endC = Math.min(Math.ceil(viewW / CELL_W), Math.ceil((sunX + rHalo + CELL_W) / CELL_W));
        const startR = Math.max(0, Math.floor((sunY - rHalo - CELL_H) / CELL_H));
        const endR = Math.min(Math.ceil(viewH / CELL_H), Math.ceil((sunY + rHalo + CELL_H) / CELL_H));

        octx.save();
        octx.font = "700 9.0px 'JetBrains Mono', monospace";
        octx.textAlign = "center";
        octx.textBaseline = "middle";

        for (let r = startR; r <= endR; r++) {
          const gy = (r + 0.5) * CELL_H;
          const dy = gy - sunY;
          for (let c = startC; c <= endC; c++) {
            const gx = (c + 0.5) * CELL_W;
            const dx = gx - sunX;
            const dist = Math.hypot(dx, dy);
            if (dist > rHalo) continue;

            // Distant Sun is always behind Mars: Mars's solid rocky globe eclipses it cleanly
            const mdx = gx - marsCx;
            const mdy = gy - marsCy;
            if (mdx * mdx + mdy * mdy < eclipseOccR2) continue;

            const norm = dist / rHalo;
            const ang = Math.atan2(dy, dx);
            const ray = 0.88 + 0.12 * Math.sin(ang * 6.0 + t * 1.6);
            const eff = norm / ray;
            if (eff > 1.0) continue;

            let ch;
            let sr, sg, sb;
            let alpha;
            if (norm < 0.26) {
              ch = (r + c) % 3 === 0 ? "@" : "#";
              sr = 255; sg = 252; sb = 235;
              alpha = 0.98;
            } else if (norm < 0.44) {
              ch = "*";
              sr = 255; sg = 226; sb = 144;
              alpha = 0.86;
            } else if (eff < 0.72) {
              ch = "+";
              sr = 255; sg = 188; sb = 96;
              alpha = (1.0 - (eff - 0.38) / 0.62) * 0.64;
            } else {
              ch = eff < 0.86 ? ":" : "·";
              sr = 255; sg = 150; sb = 76;
              alpha = (1.0 - eff) * 0.92;
            }

            alpha = Math.min(0.98, alpha * sunVis);
            if (alpha < 0.04) continue;

            octx.fillStyle = `rgba(${sr}, ${sg}, ${sb}, ${alpha.toFixed(3)})`;
            octx.fillText(ch, gx, gy);
          }
        }
        octx.restore();
      }

      function render(dt, t) {
        if (!textures.cloud || !textures.neon) return;

        const isHeroMars = activeLogo === "mars";
        if (!isHeroMars) {
          stepWaterPDE(dt);
        }
        stepBuoyantBodies(dt, t);

        octx.save();
        octx.scale(dpr, dpr);

        const fgParX = -ptrSmoothX * (isHeroMars ? 8.0 : 14.0);
        const fgParY = -ptrSmoothY * (isHeroMars ? 6.0 : 10.0);

        // True perspective projection of the distant Sun as the spacecraft camera orbits Mars:
        // Visible ONLY in the forward hemisphere (sunZ < 0, behind Mars); exits smoothly offscreen when behind camera (sunZ >= 0)
        let marsCx = viewW * 0.5 + fgParX;
        let marsCy = viewH * 0.47 + fgParY;
        let marsRadiusPx = OBJ_DRAW_W * 0.5 * 0.84;
        let sunScreenX = marsCx;
        let sunScreenY = marsCy;
        let sunVis = 0;
        if (isHeroMars && bodies.length > 0) {
          marsCx = bodies[0].x + fgParX;
          marsCy = bodies[0].y + fgParY;
          const sunZ = MARS_SUN[2];
          if (sunZ < -0.04) {
            const forwardDepth = -sunZ;
            const fovScale = Math.max(viewW, viewH * 0.62) * 0.44;
            sunScreenX = marsCx + (MARS_SUN[0] / forwardDepth) * fovScale;
            sunScreenY = marsCy + (MARS_SUN[1] / forwardDepth) * fovScale;
            const offCenter = Math.abs(sunScreenX - viewW * 0.5) / Math.max(1, viewW * 0.5);
            const inFrame = Math.max(0, Math.min(1, 1.55 - offCenter * 0.65));
            sunVis = inFrame * Math.min(1.0, (forwardDepth - 0.04) * 3.5);
          }
        }

        // 1. Deep velvet obsidian-midnight canvas (distant solar haze only when Sun is near/in forward sky)
        if (isHeroMars) {
          const glowX = sunVis > 0.01 ? sunScreenX : viewW * 0.5;
          const glowY = sunVis > 0.01 ? sunScreenY : viewH * 0.47;
          const bgSpace = octx.createRadialGradient(
            glowX, glowY, 18,
            glowX, glowY, Math.hypot(viewW, viewH) * 0.72
          );
          if (sunVis > 0.01) {
            const sunGlowA = 0.17 * sunVis;
            bgSpace.addColorStop(0, `rgba(74, 44, 24, ${sunGlowA.toFixed(3)})`);
            bgSpace.addColorStop(0.28, "#080B14");
            bgSpace.addColorStop(0.66, "#04060D");
            bgSpace.addColorStop(1, "#020308");
          } else {
            bgSpace.addColorStop(0, "#080B14");
            bgSpace.addColorStop(0.55, "#04060D");
            bgSpace.addColorStop(1, "#020308");
          }
          octx.fillStyle = bgSpace;
          octx.fillRect(0, 0, viewW, viewH);
        } else {
          const bg = octx.createRadialGradient(
            viewW * 0.5, viewH * 0.45, 40,
            viewW * 0.5, viewH * 0.5, Math.hypot(viewW, viewH) * 0.68
          );
          bg.addColorStop(0, "#0A1120");
          bg.addColorStop(0.55, "#060B15");
          bg.addColorStop(1, "#04070E");
          octx.fillStyle = bg;
          octx.fillRect(0, 0, viewW, viewH);
        }

        // 2. Deep-space starfield panning smoothly in lockstep with the orbiting camera (Mars) OR far parallax layer
        octx.textAlign = "center";
        octx.textBaseline = "middle";
        const angelFrame = Math.floor(modPos(t * 8.0, ANGEL_FRAMES));

        if (isHeroMars) {
          octx.font = "500 10.5px 'JetBrains Mono', monospace";
          const occR2 = (marsRadiusPx + 2) * (marsRadiusPx + 2);
          const skyPan = marsSunAngle / (Math.PI * 2); // distant stars & Sun move together as camera orbits Mars
          for (let i = 0; i < marsStars.length; i++) {
            const st = marsStars[i];
            const sx = modPos((st.nx + skyPan) * viewW - ptrSmoothX * (3.0 + st.depth * 11.0), viewW);
            const sy = modPos(st.ny * viewH - ptrSmoothY * (2.5 + st.depth * 8.5), viewH);
            const dx = sx - marsCx;
            const dy = sy - marsCy;
            // Solid planet blocks background stars behind both sunlit & dark hemispheres
            if (dx * dx + dy * dy < occR2) continue;
            const tw = 0.40 + 0.60 * Math.pow(0.5 + 0.5 * Math.sin(t * st.speed + st.phase), 2);
            const a = (0.14 + 0.52 * st.depth) * tw;
            octx.fillStyle = `rgba(${st.tint[0]}, ${st.tint[1]}, ${st.tint[2]}, ${a.toFixed(3)})`;
            octx.fillText(st.ch, sx, sy);
          }

          // Pure monospace ASCII shooting stars streaking across deep space (behind Mars)
          stepAndDrawMarsMeteors(dt, t, marsCx, marsCy, marsRadiusPx);

          // Distant Sun is ALWAYS behind Mars in space (drawn before Mars & eclipsed cleanly behind it)
          if (sunVis > 0.01) {
            drawDistantAsciiSun(sunScreenX, sunScreenY, sunVis, marsCx, marsCy, marsRadiusPx, t);
          }

          // Opaque dark planetary body mask so solar glow never bleeds through the solid rocky night side
          octx.save();
          octx.beginPath();
          octx.arc(marsCx, marsCy, Math.max(1, marsRadiusPx - 2), 0, Math.PI * 2);
          octx.fillStyle = "#03050B";
          octx.fill();
          octx.restore();
        } else {
          octx.font = "600 6.1px 'JetBrains Mono', monospace";
          const bgCellW = CELL_W * 0.60;
          const bgCellH = CELL_H * 0.60;
          const bgWrapX = BG_DRAW_W * 0.62 + 24;
          const bgWrapY = BG_DRAW_W * 0.62 + 24;
          const bgParX = -ptrSmoothX * 5.0;
          const bgParY = -ptrSmoothY * 4.0;

          for (let i = 0; i < bgBodies.length; i++) {
            const b = bgBodies[i];
            const bx = b.x + bgParX;
            const by = b.y + bgParY;
            const xs = [bx];
            if (bx < bgWrapX) xs.push(bx + BG_SPAN_X);
            if (bx > viewW - bgWrapX) xs.push(bx - BG_SPAN_X);
            const ys = [by];
            if (by < bgWrapY) ys.push(by + BG_SPAN_Y);
            if (by > viewH - bgWrapY) ys.push(by - BG_SPAN_Y);

            for (let xi = 0; xi < xs.length; xi++) {
              for (let yi = 0; yi < ys.length; yi++) {
                drawBuoyantBody(b, xs[xi], ys[yi], t, angelFrame, BG_DRAW_W, bgCellW, bgCellH, 0.16, true);
              }
            }
          }

          // 3. Pure 8x10 monospace ASCII water waves (water modes only; Mars is pure deep space)
          drawAsciiWaterWaves(t, angelFrame, fgParX, fgParY);
        }

        // 4. Primary full-bleed continuous rigid-shape translucent ASCII objects (or solo rotating Hero Mars)
        octx.font = "700 9.6px 'JetBrains Mono', monospace";
        const wrapX = OBJ_DRAW_W * 0.65 + 28;
        const wrapY = OBJ_DRAW_W * 0.65 + 28;
        const fgAlpha = isHeroMars ? 0.95 : 0.74;

        for (let i = 0; i < bodies.length; i++) {
          const b = bodies[i];
          const bx = b.x + fgParX;
          const by = b.y + fgParY;
          const xs = [bx];
          const ys = [by];
          if (!isHeroMars) {
            if (bx < wrapX) xs.push(bx + SPAN_X);
            if (bx > viewW - wrapX) xs.push(bx - SPAN_X);
            if (by < wrapY) ys.push(by + SPAN_Y);
            if (by > viewH - wrapY) ys.push(by - SPAN_Y);
          }

          for (let xi = 0; xi < xs.length; xi++) {
            for (let yi = 0; yi < ys.length; yi++) {
              drawBuoyantBody(b, xs[xi], ys[yi], t, angelFrame, OBJ_DRAW_W, CELL_W, CELL_H, fgAlpha, false);
            }
          }
        }

        // 5. Whisper-delicate winter snow (non-Mars water modes only)
        if (!isHeroMars) {
          octx.font = "500 11.5px 'JetBrains Mono', monospace";
          for (let i = 0; i < snowflakes.length; i++) {
            const sf = snowflakes[i];
            const pde = sampleFluidPDE(sf.x, sf.y);
            sf.x = modPos(sf.x + (sf.vxBase - pde.gx * 72.0) * dt, viewW);
            sf.y = modPos(sf.y + (sf.vyBase - pde.gy * 72.0) * dt, viewH);

            const tw = 0.45 + 0.55 * Math.pow(0.5 + 0.5 * Math.sin(t * 1.5 + sf.phase), 2);
            const a = Math.min(0.76, (0.13 + 0.32 * sf.depth) * tw + Math.abs(pde.h) * 0.42);
            if (sf.tint) {
              octx.fillStyle = `rgba(${sf.tint[0]}, ${sf.tint[1]}, ${sf.tint[2]}, ${(a * 0.85).toFixed(2)})`;
            } else {
              octx.fillStyle = `rgba(218, 232, 250, ${a.toFixed(2)})`;
            }
            octx.fillText(sf.ch, sf.x, sf.y);
          }
        }

        octx.restore();

        // 6. Subtle refined optical bloom (airy translucent mist halo, never harsh neon)
        ctx.drawImage(offCanvas, 0, 0);

        bctx.clearRect(0, 0, bloomCanvas.width, bloomCanvas.height);
        bctx.filter = "blur(6px) brightness(1.06)";
        bctx.drawImage(offCanvas, 0, 0, bloomCanvas.width, bloomCanvas.height);
        bctx.filter = "none";

        ctx.save();
        ctx.globalCompositeOperation = "lighter";
        ctx.globalAlpha = 0.24;
        ctx.drawImage(bloomCanvas, 0, 0, canvas.width, canvas.height);
        ctx.restore();

        // 7. Ultra-slow velvety midnight veil during mode transitions (cosine S-curve)
        if (fadePhase !== "idle") {
          let veil = 0;
          if (fadePhase === "out") {
            const p = Math.min(1, fadeT / FADE_OUT_SEC);
            veil = 0.5 - 0.5 * Math.cos(Math.PI * p);
          } else if (fadePhase === "hold") {
            veil = 1.0;
          } else if (fadePhase === "in") {
            const p = Math.min(1, fadeT / Math.max(0.05, fadeInDur));
            veil = 0.5 + 0.5 * Math.cos(Math.PI * p);
          }
          if (veil > 0.003) {
            ctx.save();
            ctx.fillStyle = `rgba(4, 7, 14, ${veil.toFixed(3)})`;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.restore();
          }
        }
      }

      function stepAutoRotate(dt) {
        if (fadePhase === "out") {
          fadeT += dt;
          if (fadeT >= FADE_OUT_SEC) {
            const nextKey = pendingNextLogo;
            pendingNextLogo = null;
            if (nextKey) selectLogo(nextKey, true);
            fadePhase = "hold";
            fadeT = 0;
          }
          return;
        }
        if (fadePhase === "hold") {
          fadeT += dt;
          if (fadeT >= FADE_HOLD_SEC) {
            fadePhase = "in";
            fadeInDur = FADE_IN_SEC;
            fadeT = 0;
          }
          return;
        }
        if (fadePhase === "in") {
          fadeT += dt;
          if (fadeT >= fadeInDur) {
            fadePhase = "idle";
            fadeT = 0;
          }
          return;
        }
        if (!autoRotateEnabled) return;
        const holdSec = getModeDuration(activeLogo);
        if (pointerDown) {
          // Pause switching while user is actively pressing or dragging
          autoRotateElapsed = Math.min(autoRotateElapsed, holdSec - 0.6);
          return;
        }
        autoRotateElapsed += dt;
        if (autoRotateElapsed >= holdSec) {
          const idx = MODE_ORDER.indexOf(activeLogo);
          pendingNextLogo = MODE_ORDER[(idx + 1) % MODE_ORDER.length];
          fadePhase = "out";
          fadeT = 0;
          autoRotateElapsed = 0;
        }
      }

      function tick(now) {
        const dt = Math.min(0.04, Math.max(0.001, (now - lastTs) / 1000));
        lastTs = now;
        simTime += dt;
        stepAutoRotate(dt);
        render(dt, simTime);
        requestAnimationFrame(tick);
      }

      const cloudImg = new Image();
      cloudImg.onload = () => {
        const initAll = () => {
          textures.cloud = buildCloudTexture(cloudImg);
          textures.neon = buildBannerAsciiTexture(
            "NEON",
            "& BEYOND",
            "NEONANDBEYOND",
            "gemini"
          );
          textures.japac = buildBannerAsciiTexture(
            "JAPAC",
            "CLOUD TECHIES",
            "JAPACCLOUDTECHIES",
            [
              [[0.0, "#4285F4"], [0.35, "#EA4335"], [0.68, "#FBBC04"], [1.0, "#34A853"]],
              [[0.0, "#94C8FF"], [0.5, "#FDE294"], [1.0, "#8CE2AC"]],
            ]
          );
          updateLayoutMetrics();
          for (let i = 0; i < snowflakes.length; i++) {
            snowflakes[i].x = modPos(snowflakes[i].x, viewW);
            snowflakes[i].y = modPos(snowflakes[i].y, viewH);
          }
          lastTs = performance.now();
          if (demoRipple) {
            window.setTimeout(() => {
              injectWaterDrop(viewW * 0.50, viewH * 0.48, 1.0, 2.8);
            }, 1500);
          }
          requestAnimationFrame(tick);
        };

        let booted = false;
        const safeInit = () => {
          if (booted) return;
          booted = true;
          initAll();
        };

        if (document.fonts && document.fonts.ready) {
          document.fonts.ready.then(safeInit, safeInit);
          window.setTimeout(safeInit, 800);
        } else {
          safeInit();
        }
      };
      cloudImg.src = CLOUD_LOGO_URI;
    })();
  </script>
</body>
</html>
"""

FORBIDDEN_SINKS = (
    "innerHTML",
    "outerHTML",
    "document.write",
    "eval(",
    "alert(",
    "confirm(",
    "prompt(",
)

html = HTML_TEMPLATE.replace("__LOGO_B64__", logo_b64)
for sink in FORBIDDEN_SINKS:
    if sink in html:
        raise RuntimeError(f"Forbidden security sink detected in output HTML: {sink}")

OUT_HTML.write_text(html, encoding="utf-8")
print(f"Wrote {OUT_HTML} ({len(html):,} bytes)")
