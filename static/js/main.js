/**
 * main.js — Wizard & Interactivity
 * Sistem Pakar Identifikasi Penyakit Liver
 */

"use strict";

/* ── WIZARD STATE ─────────────────────────────────────── */
let currentStep = 1;
const totalSteps = 4;
let selectedCount = 0;

/* ── INIT ─────────────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  initCheckboxes();
  updateUI();
});

/* ── CUSTOM CHECKBOXES ────────────────────────────────── */
function initCheckboxes() {
  document.querySelectorAll(".symptom-checkbox").forEach(chk => {
    const labelEl = chk.previousElementSibling; // <label>
    if (!labelEl) return;

    labelEl.addEventListener("click", (e) => {
      e.preventDefault();
      toggleSymptom(chk);
    });
  });
}

function toggleSymptom(chk) {
  const targetId    = chk.getAttribute("data-target");
  const cardId      = chk.getAttribute("data-card");
  const cbId        = chk.getAttribute("data-cb");

  const hiddenInput = document.getElementById(targetId);
  const card        = document.getElementById(cardId);
  const cbBox       = document.getElementById(cbId);

  const isNowChecked = !chk.checked;
  chk.checked = isNowChecked;

  if (hiddenInput) hiddenInput.value = isNowChecked ? "true" : "false";

  if (card) card.classList.toggle("selected", isNowChecked);
  if (cbBox) cbBox.classList.toggle("checked", isNowChecked);

  // Update total count
  selectedCount = document.querySelectorAll(".symptom-checkbox:checked").length;
  updateSelectedSummary();
}

/* ── STEP NAVIGATION ─────────────────────────────────── */
function goStep(stepNum) {
  // Hide current
  const currentEl = document.getElementById(`step-${currentStep}`);
  if (currentEl) currentEl.classList.remove("active");

  // Update indicator: mark previous as done
  updateStepIndicators(currentStep, stepNum);

  currentStep = stepNum;

  // Show new
  const newEl = document.getElementById(`step-${currentStep}`);
  if (newEl) {
    newEl.classList.add("active");
    // Scroll to top of form
    newEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  updateUI();
}

function updateStepIndicators(fromStep, toStep) {
  for (let i = 1; i <= totalSteps; i++) {
    const ind = document.querySelector(`.step-ind[data-step="${i}"]`);
    if (!ind) continue;

    if (i < toStep) {
      ind.classList.remove("active");
      ind.classList.add("done");
      const circle = ind.querySelector(".step-ind-circle");
      if (circle) circle.innerHTML = '<i class="bi bi-check-lg"></i>';
    } else if (i === toStep) {
      ind.classList.add("active");
      ind.classList.remove("done");
      const circle = ind.querySelector(".step-ind-circle");
      if (circle) circle.innerHTML = i;
    } else {
      ind.classList.remove("active", "done");
      const circle = ind.querySelector(".step-ind-circle");
      if (circle) circle.innerHTML = i;
    }
  }
}

/* ── PROGRESS BAR ────────────────────────────────────── */
function updateUI() {
  const pct = Math.round((currentStep / totalSteps) * 100);

  const progressBar = document.getElementById("wizardProgress");
  const currentStepEl = document.getElementById("currentStep");
  const progressPct = document.getElementById("progressPct");

  if (progressBar) progressBar.style.width = pct + "%";
  if (currentStepEl) currentStepEl.textContent = currentStep;
  if (progressPct) progressPct.textContent = pct;

  updateSelectedSummary();
}

/* ── SELECTED SUMMARY ────────────────────────────────── */
function updateSelectedSummary() {
  selectedCount = document.querySelectorAll(".symptom-checkbox:checked").length;
  const summaryEl = document.getElementById("selectedSummary");
  const countEl   = document.getElementById("selectedCount");

  if (summaryEl) summaryEl.style.display = selectedCount > 0 ? "block" : "none";
  if (countEl)   countEl.textContent = selectedCount;
}

/* ── RESET FORM ──────────────────────────────────────── */
function resetForm() {
  // Uncheck all
  document.querySelectorAll(".symptom-checkbox").forEach(chk => {
    chk.checked = false;
  });

  // Reset hidden inputs
  document.querySelectorAll("[id^='hidden-']").forEach(inp => {
    inp.value = "false";
  });

  // Reset card states
  document.querySelectorAll(".symptom-card").forEach(card => {
    card.classList.remove("selected");
  });

  // Reset checkbox visuals
  document.querySelectorAll(".custom-checkbox").forEach(cb => {
    cb.classList.remove("checked");
  });

  selectedCount = 0;
  updateSelectedSummary();

  // Go back to step 1
  goStep(1);
}

/* ── FORM SUBMIT ─────────────────────────────────────── */
const form = document.getElementById("symptomForm");
if (form) {
  form.addEventListener("submit", (e) => {
    const btn = document.getElementById("submitBtn");
    if (btn) {
      btn.querySelector(".btn-process-content")?.classList.add("d-none");
      btn.querySelector(".btn-process-loading")?.classList.remove("d-none");
      btn.disabled = true;
    }
  });
}
