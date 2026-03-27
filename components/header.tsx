import Image from "next/image"

export default function Header() {
  return (
    <header className="fixed top-0 left-0 w-full z-50 bg-neutral-700 backdrop-blur-md border-b border-white/20">
      <div className="mx-auto px-6 h-16 flex items-center justify-between" style={{ maxWidth: "1200px" }}>
        <div className="flex items-center gap-3">
          <Image
            src="/lava lamp logo.png"
            alt="EntropyLab logo"
            width={40}
            height={40}
            className="h-10 w-10 object-contain"
          />
          <div className="text-xl font-bold tracking-tight text-neutral-  0">
            Entropy<span className="text-red-600">Lab</span>
          </div>
        </div>
        <nav className="flex items-center gap-8">
          <a href="#" className="text-sm font-medium text-neutral-0 hover:text-teal-600 transition-colors">Como funciona</a>
          <a href="#" className="text-sm font-medium text-neutral-0 hover:text-teal-600 transition-colors">Documentación</a>
          <a href="#" className="text-sm font-medium text-neutral-0 hover:text-teal-600 transition-colors">Github</a>
          <a
            href="#"
            className="rounded-full bg-red-600 px-5 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700"
          >
            Obtener claves
          </a>
        </nav>
      </div>
    </header>
  )
}
