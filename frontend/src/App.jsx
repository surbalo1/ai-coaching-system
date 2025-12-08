import { useState } from 'react'
import { LayoutDashboard, Mic2, Bot, Video, Send, Users } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'

import SourcingView from './components/SourcingView'
import CoachView from './components/CoachView'
import MediaView from './components/MediaView'
import OutreachView from './components/OutreachView'

const DashboardHome = () => (
  <div className="space-y-6">
    <h1 className="text-4xl font-bold text-white mb-2">Welcome Back, Coach.</h1>
    <p className="text-gray-400 mb-8 text-lg">Your AI systems are running optimally.</p>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <Link to="/sourcing" className="glass-panel p-8 hover:bg-white/5 transition-all cursor-pointer group">
        <div className="bg-purple-500/20 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <Mic2 className="text-purple-400" />
        </div>
        <h3 className="text-xl font-bold text-white mb-2">Find Guests</h3>
        <p className="text-gray-400">Scrape podcasts and find leads.</p>
      </Link>

      <Link to="/coach" className="glass-panel p-8 hover:bg-white/5 transition-all cursor-pointer group">
        <div className="bg-blue-500/20 w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
          <Bot className="text-blue-400" />
        </div>
        <h3 className="text-xl font-bold text-white mb-2">Ask AI Coach</h3>
        <p className="text-gray-400">Query your knowledge base.</p>
      </Link>
    </div>
  </div>
)

const NavItem = ({ to, icon: Icon, label }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link to={to} style={{ textDecoration: 'none' }}>
      <div className={`flex items-center gap-3 p-3 rounded-lg mb-2 cursor-pointer transition-all ${isActive ? 'bg-white/10 text-white' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}>
        <Icon size={20} color={isActive ? '#8b5cf6' : 'currentColor'} />
        <span className="font-medium">{label}</span>
      </div>
    </Link>
  )
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <aside className="sidebar">
          <div className="mb-10 px-2">
            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              ANTIGRAVITY<span className="text-white text-xs block opacity-50">AI SYSTEMS</span>
            </h2>
          </div>

          <nav>
            <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
            <NavItem to="/sourcing" icon={Mic2} label="Speaker Sourcing" />
            <NavItem to="/coach" icon={Bot} label="AI Coach" />
            <NavItem to="/media" icon={Video} label="Content Engine" />
            <NavItem to="/outreach" icon={Send} label="Outreach" />
            <NavItem to="/crm" icon={Users} label="CRM" />
          </nav>
        </aside>

        <main className="main-content">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<DashboardHome />} />
              <Route path="/sourcing" element={<SourcingView />} />
              <Route path="/coach" element={<CoachView />} />
              <Route path="/media" element={<MediaView />} />
              <Route path="/outreach" element={<OutreachView />} />
              <Route path="/crm" element={<OutreachView />} /> {/* Reusing Outreach for now */}
            </Routes>
          </AnimatePresence>
        </main>
      </div>
    </Router>
  )
}

export default App
