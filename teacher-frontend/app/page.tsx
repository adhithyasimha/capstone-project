"use client"

import { useState } from "react"
import { Navbar } from "@/components/navbar"
import { Sidebar } from "@/components/sidebar"
import { DashboardContent } from "@/components/dashboard-content"
import CodeReplayContent from "@/components/codereplay-content"
import { ReportsContent } from "@/components/reports-content"

export default function Dashboard() {
  const [activeSection, setActiveSection] = useState("dashboard")

  const renderContent = () => {
    switch (activeSection) {
      case "dashboard":
        return <DashboardContent />
      case "codereplay":
        return <CodeReplayContent />
      case "reports":
        return <ReportsContent />
      default:
        return <DashboardContent />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex">
        <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
        <main className="flex-1 p-6">{renderContent()}</main>
      </div>
    </div>
  )
}
