import React from 'react'
import './styles/index.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Rec-Buddy | Recovery Trainer',
  description: 'Your AI personal trainer for physical recovery',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="glow-mesh"></div>
        {children}
      </body>
    </html>
  )
}
