import { useState } from 'react'
import AddEmployeeForm from './components/AddEmployeeForm'
import EmployeeList from './components/EmployeeList'

function App() {
  const [refreshKey, setRefreshKey] = useState(0)

  const handleEmployeeAdded = () => {
    // Increment key so EmployeeList re-fetches data
    setRefreshKey((prev) => prev + 1)
  }

  return (
    <div className="page-wrap">
      <AddEmployeeForm onEmployeeAdded={handleEmployeeAdded} />
      <EmployeeList refreshKey={refreshKey} />
    </div>
  )
}

export default App
