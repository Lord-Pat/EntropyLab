"use client"

export default function VideoBackground() {
  return (
    <div
      className="pointer-events-none absolute inset-0 z-[-1] overflow-hidden bg-black"
      style={{ backgroundColor: "#5b3222" }}
    >
      <div className="absolute inset-0" style={{ mixBlendMode: "difference" }}>
        <video
          autoPlay
          loop
          muted
          playsInline
          preload="auto"
          aria-hidden="true"
          className="h-full w-full object-cover"
        >
          <source src="/lava_lamp_bg.mp4" type="video/mp4" />
        </video>
      </div>
    </div>
  )
}
