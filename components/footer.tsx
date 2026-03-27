export default function Footer() {
  return (
    <footer className="bg-teal-900 py-12">
      <div className="mx-auto px-6 flex justify-between items-center" style={{ maxWidth: "1200px" }}>
        <div className="text-xl font-bold text-white">Logo</div>
        <nav className="flex justify-between gap-12">
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Inicio</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Nosotros</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Servicios</a>
          <a href="#" className="text-sm text-teal-100 hover:text-white transition-colors">Contacto</a>
        </nav>
      </div>
    </footer>
  )
}
