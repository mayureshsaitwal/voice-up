import Dashboard from "@/pages/Dashboard"
import AppSidebar from "./components/Sidebar"
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { BrowserRouter, Routes, Route } from "react-router";
import Chats from "./pages/Chats.tsx"

function App() {
  return (
    <main className="min-h-screen bg-background text-foreground font-sans antialiased">
      <SidebarProvider>
        <AppSidebar />
        <BrowserRouter>
          <Routes>
            <Route path="/home" element={<Dashboard />} />
            <Route path="/chats" element={<Chats />} />
            {/* <Dashboard /> */}
          </Routes>
        </BrowserRouter>
      </SidebarProvider>
    </main>
  )
}

export default App
