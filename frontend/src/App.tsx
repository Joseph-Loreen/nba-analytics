import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import PlayerProfile from './pages/PlayerProfile'
import TeamPage from './pages/TeamPage'

function App() {
  return (
    <BrowserRouter>
      <nav className="bg-gray-900 text-white p-4 flex gap-4">
        <Link to="/">Home</Link>
        <Link to="/players/237">Sample Player</Link>
        <Link to="/teams/14">Sample Team</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/players/:playerId" element={<PlayerProfile />} />
        <Route path="/teams/:teamId" element={<TeamPage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App