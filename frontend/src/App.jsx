import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import EmployeeList from './components/EmployeeList'

function App() {
  return (
    <BrowserRouter>
      <div className="page-wrap">
        <Routes>
          {/* Redirect root path to employees page */}
          <Route path="/" element={<Navigate to="/employees" replace />} />

          {/* Main page that shows all employees */}
          <Route path="/employees" element={<EmployeeList />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App
