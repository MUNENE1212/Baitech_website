import { useState, useEffect } from "react";

export default function AdminDashboard() {
  const [services, setServices] = useState([]);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    fetchServices();
  }, [filter]);

  const fetchServices = async () => {
    const response = await fetch(
      `http://127.0.0.1:8000/admin/services?status=${filter}`
    );
    const data = await response.json();
    setServices(data);
  };

  const updateStatus = async (id, newStatus) => {
    await fetch(`http://127.0.0.1:8000/services/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    fetchServices();
  };

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold">Admin Service Dashboard</h1>
      <select onChange={(e) => setFilter(e.target.value)} className="mt-2">
        <option value="">All</option>
        <option value="Pending">Pending</option>
        <option value="In Progress">In Progress</option>
        <option value="Completed">Completed</option>
      </select>

      <table className="w-full mt-4 border">
        <thead>
          <tr className="bg-gray-200">
            <th>Customer</th>
            <th>Service Type</th>
            <th>Item</th>
            <th>Status</th>
            <th>Update</th>
          </tr>
        </thead>
        <tbody>
          {services.map((service) => (
            <tr key={service._id} className="border-t">
              <td>{service.customer_name}</td>
              <td>{service.service_type}</td>
              <td>{service.item || "N/A"}</td>
              <td>{service.status}</td>
              <td>
                <button onClick={() => updateStatus(service._id, "In Progress")}>
                  Start
                </button>
                <button onClick={() => updateStatus(service._id, "Completed")}>
                  Complete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
