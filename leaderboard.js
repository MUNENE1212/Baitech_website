import { useState, useEffect } from "react";

export default function Leaderboard() {
  const [technicians, setTechnicians] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/leaderboard")
      .then((res) => res.json())
      .then((data) => setTechnicians(data));
  }, []);

  return (
    <div className="p-5">
      <h1 className="text-xl font-bold">Technician Leaderboard 🏆</h1>
      <table className="w-full mt-4 border">
        <thead>
          <tr className="bg-gray-200">
            <th>Name</th>
            <th>Specialization</th>
            <th>Jobs Completed</th>
            <th>Rating</th>
          </tr>
        </thead>
        <tbody>
          {technicians.map((tech) => (
            <tr key={tech._id} className="border-t">
              <td>{tech.name}</td>
              <td>{tech.specializations.join(", ")}</td>
              <td>{tech.jobs_completed}</td>
              <td>{tech.average_rating.toFixed(1)} ⭐</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
