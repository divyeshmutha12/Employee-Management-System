import { useEffect, useState } from 'react'
import axios from 'axios'
import { Alert, Button, Card, List, Popconfirm, Space, Tag, Typography } from 'antd'

const { Title, Text } = Typography
const API_BASE_URL = 'http://127.0.0.1:8000'

function EmployeeList({ refreshKey = 0 }) {
  const [employees, setEmployees] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [deletingId, setDeletingId] = useState(null)

  const fetchEmployees = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await axios.get(`${API_BASE_URL}/employees`)
      setEmployees(response.data)
    } catch (err) {
      console.error('Failed to fetch employees:', err)
      setError('Could not load employees. Please check backend and try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchEmployees()
  }, [refreshKey])

  const handleDelete = async (employeeId) => {
    try {
      setDeletingId(employeeId)
      setError('')
      await axios.delete(`${API_BASE_URL}/employees/${employeeId}`)
      setEmployees((prev) => prev.filter((employee) => employee.id !== employeeId))
    } catch (err) {
      console.error('Failed to delete employee:', err)
      setError('Could not delete employee. Please try again.')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <Card className="employee-card" style={{ marginTop: 16 }}>
      <Title level={3} style={{ marginTop: 0, marginBottom: 6 }}>
        Employee List
      </Title>
      <Text type="secondary">View all employees and delete if needed.</Text>

      {error && (
        <Alert
          style={{ marginTop: 16 }}
          type="error"
          showIcon
          message={error}
        />
      )}

      <List
        loading={loading}
        style={{ marginTop: 16 }}
        dataSource={employees}
        locale={{ emptyText: 'No employees found.' }}
        renderItem={(employee) => (
          <List.Item
            actions={[
              <Popconfirm
                key={employee.id}
                title="Delete employee"
                description="Are you sure you want to delete this employee?"
                onConfirm={() => handleDelete(employee.id)}
                okText="Yes"
                cancelText="No"
              >
                <Button danger loading={deletingId === employee.id}>
                  Delete
                </Button>
              </Popconfirm>,
            ]}
          >
            <Space direction="vertical" size={2}>
              <Text strong>{employee.name}</Text>
              <Tag color="blue">{employee.role}</Tag>
            </Space>
          </List.Item>
        )}
      />
    </Card>
  )
}

export default EmployeeList
