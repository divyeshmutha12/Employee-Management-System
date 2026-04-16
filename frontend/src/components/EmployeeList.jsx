import { useEffect, useState } from 'react'
import axios from 'axios'
import { Alert, Card, List, Spin, Tag, Typography } from 'antd'

const { Title, Text } = Typography

// FastAPI base URL (update this when deploying)
const API_BASE_URL = 'http://127.0.0.1:8000'

function EmployeeList() {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    // Load employee data once when this component mounts
    const fetchEmployees = async () => {
      try {
        setLoading(true)
        setError('')

        const response = await axios.get(`${API_BASE_URL}/employees`)
        setEmployees(response.data)
      } catch (err) {
        console.error('Failed to fetch employees:', err)
        setError('Could not load employees. Please check if backend is running.')
      } finally {
        setLoading(false)
      }
    }

    fetchEmployees()
  }, [])

  return (
    <Card className="employee-card">
      <Title level={3} style={{ marginTop: 0 }}>Employee List</Title>
      <Text type="secondary">Showing employees from FastAPI backend</Text>

      {loading && (
        <div className="state-box">
          <Spin size="large" />
          <Text>Loading employees...</Text>
        </div>
      )}

      {!loading && error && (
        <Alert
          message="Error"
          description={error}
          type="error"
          showIcon
          style={{ marginTop: 16 }}
        />
      )}

      {!loading && !error && (
        <List
          style={{ marginTop: 16 }}
          dataSource={employees}
          locale={{ emptyText: 'No employees found.' }}
          renderItem={(employee) => (
            <List.Item>
              <div className="employee-row">
                <Text strong>{employee.name}</Text>
                <Tag color="blue">{employee.role}</Tag>
              </div>
            </List.Item>
          )}
        />
      )}
    </Card>
  )
}

export default EmployeeList
