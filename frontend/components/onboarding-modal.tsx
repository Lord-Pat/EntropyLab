"use client"

import { useEffect, useMemo, useState } from "react"
import { toast } from "sonner"

import styles from "./onboarding-modal.module.css"

type OnboardingModalProps = {
  isOpen: boolean
  onClose: () => void
  onSuccess?: (quantity: number) => void
}


const TITLES = [
  "&iquest;Cu&aacute;ntas claves necesitas?",
  "Formato de exportaci&oacute;n",
  "Obtenci&oacute;n y env&iacute;o",
  "Confirmar y generar",
]

const EYES = ["Paso 1 de 4", "Paso 2 de 4", "Paso 3 de 4", "Paso 4 de 4"]
const STEP_LABELS = ["Cantidad", "Formato", "Envío", "Confirmar"]

const quantityOptions = [1, 5, 10, 15, 20]

type ExportType = "csv" | "json" | "txt" | null
type DeliveryType = "download" | "email" | null

export default function OnboardingModal({ isOpen, onClose, onSuccess }: OnboardingModalProps) {
  const [step, setStep] = useState(1)
  const [selQty, setSelQty] = useState<number | null>(null)
  const [selExport, setSelExport] = useState<ExportType>(null)
  const [selDelivery, setSelDelivery] = useState<DeliveryType>(null)
  const [accOpen, setAccOpen] = useState(false)
  const [email, setEmail] = useState("")
  const [isSuccess, setIsSuccess] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (!isOpen) {
      return
    }

    setStep(1)
    setSelQty(null)
    setSelExport(null)
    setSelDelivery(null)
    setAccOpen(false)
    setEmail("")
    setIsSuccess(false)
    setIsSubmitting(false)
  }, [isOpen])

  useEffect(() => {
    if (!isSuccess) {
      return
    }

    const timeout = window.setTimeout(() => {
      onClose()
    }, 1800)

    return () => window.clearTimeout(timeout)
  }, [isSuccess, onClose])

  const isEmailValid = useMemo(() => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email), [email])

  const isNextDisabled = useMemo(() => {
    if (step === 1) return !selQty
    if (step === 2) return !selExport
    if (step === 3) {
      if (!selDelivery) return true
      if (selDelivery === "email") return !isEmailValid
      return false
    }
    return false
  }, [isEmailValid, selDelivery, selExport, selQty, step])

  if (!isOpen) {
    return null
  }

  const API_URL = process.env.NEXT_PUBLIC_API_URL

  const goNext = async () => {
    if (step === 4) {
      try {
        if (selDelivery === "download") {
          const response = await fetch(
            `${API_URL}/keys/generate?cantidad=${selQty}&formato=${selExport}`,
            { method: "POST" }
          )

          if (!response.ok) throw new Error("Error generando claves")

          if (selExport === "json") {
            const data = await response.json()
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
            const url = URL.createObjectURL(blob)
            const a = document.createElement("a")
            a.href = url
            a.download = `entropylab-keys-${Date.now()}.json`
            a.click()
            URL.revokeObjectURL(url)
          } else {
            const blob = await response.blob()
            const url = URL.createObjectURL(blob)
            const a = document.createElement("a")
            a.href = url
            a.download = `entropylab-keys-${Date.now()}.${selExport}`
            a.click()
            URL.revokeObjectURL(url)
          }
        }

        if (selDelivery === "email") {
          const response = await fetch(
            `${API_URL}/keys/send-email?cantidad=${selQty}&formato=${selExport}&email=${encodeURIComponent(email)}`,
            { method: "POST" }
          )
          if (!response.ok) throw new Error("Error enviando email")
        }

        onSuccess?.(selQty ?? 1)
        toast.success(`${selQty ?? 1} clave${(selQty ?? 1) > 1 ? "s" : ""} generada${(selQty ?? 1) > 1 ? "s" : ""} correctamente`)
        setIsSuccess(true)

      } catch (error) {
        toast.error("Error conectando con el servidor. Verifica que la API está activa.")
      }
      return
    }

    if (!isNextDisabled) {
      setStep((current) => current + 1)
    }
  }
  const goBack = () => {
    setStep((current) => Math.max(1, current - 1))
  }

  const selectQty = (value: number) => {
    setSelQty(value)
    setAccOpen(false)
  }

  const selectExport = (value: Exclude<ExportType, null>) => {
    setSelExport(value)
  }

  const selectDelivery = (value: Exclude<DeliveryType, null>) => {
    setSelDelivery(value)
    if (value !== "email") {
      setEmail("")
    }
  }

  const qtyLabel = selQty ? `${selQty} clave${selQty > 1 ? "s" : ""}` : "—"
  const fmtLabel = selExport ? selExport.toUpperCase() : "—"
  const deliveryLabel = selDelivery === "download" ? "Descarga directa" : selDelivery === "email" ? "Email" : "—"

  return (
    <div className={`${styles.overlay} ${isOpen ? styles.open : ""}`} onClick={onClose}>
      <div className={styles.modal} onClick={(event) => event.stopPropagation()}>
        <div className={styles.modalHeader}>
          <div className={styles.modalToprow}>
            <div>
              <div className={styles.modalEyebrow}>{EYES[step - 1]}</div>
              <div className={styles.modalTitle} dangerouslySetInnerHTML={{ __html: TITLES[step - 1] }} />
            </div>
            <button type="button" className={styles.modalClose} onClick={onClose} aria-label="Cerrar">
              <svg aria-hidden="true" viewBox="0 0 20 20" className={styles.modalCloseIcon}>
                <path d="m5 5 10 10M15 5 5 15" />
              </svg>
            </button>
          </div>

          <div className={styles.stepsRow}>
            {[1, 2, 3, 4].map((item, index) => (
              <div key={item} className={styles.stepGroup}>
                <div
                  className={`${styles.stepPill} ${step === item ? styles.active : ""} ${step > item ? styles.done : ""}`}
                >
                  <div
                    className={`${styles.stepCircle} ${step === item ? styles.active : ""} ${step > item ? styles.done : ""}`}
                  >
                    {step > item ? (
                      <svg aria-hidden="true" viewBox="0 0 20 20" className={styles.stepCheck}>
                        <path d="M4.5 10.5 8.25 14 15.5 5.75" />
                      </svg>
                    ) : (
                      item
                    )}
                  </div>
                  <span className={styles.stepLabel}>{STEP_LABELS[index]}</span>
                </div>
                {item < 4 && <div className={styles.stepConnector} />}
              </div>
            ))}
          </div>
        </div>

        <div className={styles.divider} />

        <div className={styles.modalBody}>
          {step === 1 && (
            <div className={`${styles.stepPanel} ${styles.active}`}>
              <p className={styles.stepSub}>
                Selecciona cuántas claves criptográficas quieres generar en esta sesión.
              </p>

              <div className={styles.accordion}>
                <button type="button" className={styles.accHeader} onClick={() => setAccOpen((current) => !current)}>
                  <div className={`${styles.accRadio} ${selQty ? styles.checked : ""}`}>
                    {selQty ? <span className={styles.innerDot} /> : null}
                  </div>
                  <span className={styles.accLabel}>{selQty ? qtyLabel : "Seleccionar cantidad"}</span>
                  <span className={`${styles.accChevron} ${accOpen ? styles.open : ""}`}>▾</span>
                </button>

                <div className={`${styles.accBody} ${accOpen ? styles.open : ""}`}>
                  <div className={styles.qtyGrid}>
                    {quantityOptions.map((option) => (
                      <button
                        key={option}
                        type="button"
                        className={`${styles.qtyOpt} ${selQty === option ? styles.selected : ""}`}
                        onClick={() => selectQty(option)}
                      >
                        {option}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className={`${styles.stepPanel} ${styles.active}`}>
              <p className={styles.stepSub}>Elige el formato en el que quieres que se generen tus claves.</p>

              <div className={styles.exportGrid}>
                <button
                  type="button"
                  className={`${styles.exportOpt} ${selExport === "csv" ? styles.selected : ""}`}
                  onClick={() => selectExport("csv")}
                >
                  <div className={styles.exportIcon}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <rect x="2" y="1" width="9" height="14" rx="1.5" fill="#333" />
                      <rect x="9" y="1" width="4" height="4" rx="0.5" fill="#2A2A2A" />
                      <rect x="4" y="7" width="7" height="1" rx="0.5" fill="#555" />
                      <rect x="4" y="9.5" width="5" height="1" rx="0.5" fill="#555" />
                    </svg>
                  </div>
                  <div>
                    <div className={styles.exportName}>CSV</div>
                    <div className={styles.exportDesc}>Hoja de cálculo</div>
                  </div>
                  <div className={`${styles.exportCheck} ${selExport === "csv" ? styles.checked : ""}`}>
                    {selExport === "csv" ? <span className={styles.innerDot} /> : null}
                  </div>
                </button>

                <button
                  type="button"
                  className={`${styles.exportOpt} ${selExport === "json" ? styles.selected : ""}`}
                  onClick={() => selectExport("json")}
                >
                  <div className={styles.exportIcon}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path
                        d="M5 3C3.5 3 3 4 3 5v2c0 1-.5 1.5-1 2 .5.5 1 1 1 2v2c0 1 .5 2 2 2"
                        stroke="#555"
                        strokeWidth="1.2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M11 3c1.5 0 2 1 2 2v2c0 1 .5 1.5 1 2-.5.5-1 1-1 2v2c0 1-.5 2-2 2"
                        stroke="#555"
                        strokeWidth="1.2"
                        strokeLinecap="round"
                      />
                    </svg>
                  </div>
                  <div>
                    <div className={styles.exportName}>JSON</div>
                    <div className={styles.exportDesc}>Estructurado</div>
                  </div>
                  <div className={`${styles.exportCheck} ${selExport === "json" ? styles.checked : ""}`}>
                    {selExport === "json" ? <span className={styles.innerDot} /> : null}
                  </div>
                </button>

                <button
                  type="button"
                  className={`${styles.exportOpt} ${styles.spanTwo} ${selExport === "txt" ? styles.selected : ""}`}
                  onClick={() => selectExport("txt")}
                >
                  <div className={styles.exportIcon}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <rect x="2" y="1" width="12" height="14" rx="1.5" fill="#333" />
                      <rect x="4" y="5" width="8" height="1" rx="0.5" fill="#555" />
                      <rect x="4" y="7.5" width="8" height="1" rx="0.5" fill="#555" />
                      <rect x="4" y="10" width="5" height="1" rx="0.5" fill="#555" />
                    </svg>
                  </div>
                  <div>
                    <div className={styles.exportName}>TXT</div>
                    <div className={styles.exportDesc}>Texto plano</div>
                  </div>
                  <div className={`${styles.exportCheck} ${selExport === "txt" ? styles.checked : ""}`}>
                    {selExport === "txt" ? <span className={styles.innerDot} /> : null}
                  </div>
                </button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className={`${styles.stepPanel} ${styles.active}`}>
              <p className={styles.stepSub}>
                Cómo quieres obtener tus claves? Descárgalas directamente o recíbelas por correo.
              </p>

              <div className={styles.exportGridNoMargin}>
                <button
                  type="button"
                  className={`${styles.exportOpt} ${selDelivery === "download" ? styles.selected : ""}`}
                  onClick={() => selectDelivery("download")}
                >
                  <div className={styles.exportIcon}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path
                        d="M8 2v8M5 7l3 3 3-3"
                        stroke="#555"
                        strokeWidth="1.3"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <rect x="2" y="12" width="12" height="2" rx="1" fill="#555" />
                    </svg>
                  </div>
                  <div>
                    <div className={styles.exportName}>Download</div>
                    <div className={styles.exportDesc}>Descarga directa</div>
                  </div>
                  <div className={`${styles.exportCheck} ${selDelivery === "download" ? styles.checked : ""}`}>
                    {selDelivery === "download" ? <span className={styles.innerDot} /> : null}
                  </div>
                </button>

                <button
                  type="button"
                  className={`${styles.exportOpt} ${selDelivery === "email" ? styles.selected : ""}`}
                  onClick={() => selectDelivery("email")}
                >
                  <div className={styles.exportIcon}>
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <rect x="1" y="3" width="14" height="10" rx="2" stroke="#555" strokeWidth="1.2" />
                      <path d="M1 5l7 5 7-5" stroke="#555" strokeWidth="1.2" strokeLinecap="round" />
                    </svg>
                  </div>
                  <div>
                    <div className={styles.exportName}>Email</div>
                    <div className={styles.exportDesc}>Enviar a tu correo</div>
                  </div>
                  <div className={`${styles.exportCheck} ${selDelivery === "email" ? styles.checked : ""}`}>
                    {selDelivery === "email" ? <span className={styles.innerDot} /> : null}
                  </div>
                </button>
              </div>

              {selDelivery === "email" && (
                <div className={styles.emailFieldWrap}>
                  <label className={styles.emailLabel} htmlFor="emailInput">
                    Dirección de correo
                  </label>
                  <input
                    id="emailInput"
                    className={styles.emailInput}
                    type="email"
                    placeholder="tu@correo.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                  />
                </div>
              )}
            </div>
          )}

          {step === 4 && (
            <div className={`${styles.stepPanel} ${styles.active}`}>
              <p className={styles.stepSub}>Revisa que todo esté correcto antes de generar tus claves.</p>

              <div className={styles.confirmCard}>
                <div className={styles.confirmRow}>
                  <span className={styles.confirmKey}>Cantidad de claves</span>
                  <span className={styles.confirmVal}>{qtyLabel}</span>
                </div>
                <div className={styles.confirmRow}>
                  <span className={styles.confirmKey}>Formato de exportación</span>
                  <span className={styles.confirmVal}>{fmtLabel}</span>
                </div>
                <div className={styles.confirmRow}>
                  <span className={styles.confirmKey}>Método de obtención</span>
                  <span className={styles.confirmVal}>{deliveryLabel}</span>
                </div>
                {selDelivery === "email" && (
                  <div className={styles.confirmRow}>
                    <span className={styles.confirmKey}>Destino email</span>
                    <span className={`${styles.confirmVal} ${styles.confirmEmail}`}>{email || "—"}</span>
                  </div>
                )}
                <div className={styles.confirmRow}>
                  <span className={styles.confirmKey}>Estado</span>
                  <span className={styles.confirmBadge}>Listo para generar</span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className={styles.divider} />

        <div className={styles.modalFooter}>
          {step > 1 ? (
            <button type="button" className={styles.btnBack} onClick={goBack}>
              Atrás
            </button>
          ) : (
            <div />
          )}

          <button
            type="button"
            className={`${styles.btnNext} ${isSuccess ? styles.success : ""}`}
            onClick={goNext}
            disabled={isNextDisabled || isSuccess || isSubmitting}
          >
            {step === 4
              ? isSuccess
                ? "Claves generadas"
                : isSubmitting
                  ? "Generando..."
                  : "Generar claves"
              : "Continuar →"}
          </button>
        </div>
      </div>
    </div>
  )
}
