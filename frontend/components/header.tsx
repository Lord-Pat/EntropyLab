"use client"

import Image from "next/image"
import Link from "next/link"
import { useState } from "react"

type HeaderProps = {
  onOpenOnboarding?: () => void
}

export default function Header({ onOpenOnboarding }: HeaderProps) {
  const [isOpen, setIsOpen] = useState(false)

  const navLinks = (
    <>
      <a
        href="/#sobre-nosotros"
        onClick={() => setIsOpen(false)}
        className="text-sm font-medium text-white outline-none transition-colors hover:text-red-400"
      >
        Sobre nosotros
      </a>
      <a
        href="https://github.com/Lord-Pat/EntropyLab"
        target="_blank"
        rel="noreferrer"
        onClick={() => setIsOpen(false)}
        className="text-sm font-medium text-white outline-none transition-colors hover:text-red-400"
      >
        Github
      </a>
      {onOpenOnboarding ? (
        <button
          type="button"
          onClick={() => { onOpenOnboarding(); setIsOpen(false) }}
          className="rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700"
        >
          Obtener claves
        </button>
      ) : (
        <Link
          href="/"
          onClick={() => setIsOpen(false)}
          className="rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700"
        >
          Obtener claves
        </Link>
      )}
    </>
  )

  return (
    <header className="fixed top-0 left-0 z-50 w-full border-b border-white/10 bg-black/40 backdrop-blur-md">
      <div
        className="mx-auto px-4 sm:px-6"
        style={{ maxWidth: "1200px" }}
      >
        {/* Top bar: logo + hamburger (mobile) / logo + nav (desktop) */}
        <div className="flex h-16 items-center justify-between">
          <a href="#" onClick={() => setIsOpen(false)} className="flex items-center gap-3">
            <Image
              src="/lava lamp logo.png"
              alt="EntropyLab logo"
              width={40}
              height={40}
              className="h-10 w-10 object-contain invert"
            />
            <div className="text-xl font-bold tracking-tight text-white">
              Entropy<span className="text-red-600">Lab</span>
            </div>
          </a>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-6">
            {navLinks}
          </nav>

          {/* Hamburger button — mobile only */}
          <button
            type="button"
            aria-label="Abrir menú"
            onClick={() => setIsOpen((v) => !v)}
            className="md:hidden flex flex-col justify-center items-center gap-1.5 p-2 text-white"
          >
            <span className={`block h-0.5 w-6 bg-white transition-transform duration-200 ${isOpen ? "translate-y-2 rotate-45" : ""}`} />
            <span className={`block h-0.5 w-6 bg-white transition-opacity duration-200 ${isOpen ? "opacity-0" : ""}`} />
            <span className={`block h-0.5 w-6 bg-white transition-transform duration-200 ${isOpen ? "-translate-y-2 -rotate-45" : ""}`} />
          </button>
        </div>

        {/* Mobile dropdown nav */}
        {isOpen && (
          <nav className="md:hidden flex flex-col gap-4 pb-4 pt-2 border-t border-white/10">
            {navLinks}
          </nav>
        )}
      </div>
    </header>
  )
}
