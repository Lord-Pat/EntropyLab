"use client"

export default function VideoBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 z-[-1] overflow-hidden bg-black">
      <div className="absolute inset-0">
        <video
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          aria-hidden="true"
          className="h-full w-full object-cover opacity-30 blur-lg"
        >
          <source src="/lava_lamp_bg.mp4" type="video/mp4" />
        </video>
      </div>

      <div className="absolute inset-0 bg-black/55" />
    </div>
  )
}
