import { useState } from "react";
import axios from "axios";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState(null);
    // Filter states
const [selectedBranch, setSelectedBranch] = useState("All");
const [selectedDepartment, setSelectedDepartment] = useState("All");
const [selectedOperator, setSelectedOperator] = useState("All");
const [selectedStatus, setSelectedStatus] = useState("All");
const [selectedClient, setSelectedClient] = useState("All");

const branchOptions = analysis
  ? Object.keys(analysis.branch_distribution)
      .filter((item) => item !== "Missing")
      .sort()
  : [];

const departmentOptions = analysis
  ? Object.keys(analysis.department_distribution)
      .filter((item) => item !== "Missing")
      .sort()
  : [];

const operatorOptions = analysis
  ? Object.keys(analysis.operator_distribution)
      .filter((item) => item !== "Missing")
      .sort()
  : [];

const statusOptions = analysis
  ? Object.keys(analysis.status_distribution)
      .filter((item) => item !== "Missing")
      .sort()
  : [];

const clientOptions = analysis
  ? Object.keys(analysis.client_distribution)
      .filter((item) => item !== "Missing")
      .sort()
  : [];

  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setError("");
    setAnalysis(null);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please select an Excel file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setError("");

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        formData
      );

      setAnalysis(response.data);
    } catch (err) {
      console.error(err);
      setError("Unable to analyse the file. Please check the backend.");
    } finally {
      setLoading(false);
    }
  };

  const filteredRecords = analysis
  ? analysis.records.filter((record) => {

      const branchMatch =
        selectedBranch === "All" ||
        record["Branch"] === selectedBranch;

      const departmentMatch =
        selectedDepartment === "All" ||
        record["Department"] === selectedDepartment;

      const operatorMatch =
        selectedOperator === "All" ||
        record["Operator"] === selectedOperator;

      const statusMatch =
        selectedStatus === "All" ||
        record["Status"] === selectedStatus;

      const clientMatch =
        selectedClient === "All" ||
        record["Client Y / N"] === selectedClient;

      return (
        branchMatch &&
        departmentMatch &&
        operatorMatch &&
        statusMatch &&
        clientMatch
      );
    })
  : [];

  const filteredTotalRecords = filteredRecords.length;

const filteredBranches = new Set(
  filteredRecords
    .map((record) => record["Branch"])
    .filter(Boolean)
).size;

const filteredDepartments = new Set(
  filteredRecords
    .map((record) => record["Department"])
    .filter(Boolean)
).size;

const filteredOperators = new Set(
  filteredRecords
    .map((record) => record["Operator"])
    .filter(Boolean)
).size;

const filteredBranchData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const branch = record["Branch"] || "Missing";
    acc[branch] = (acc[branch] || 0) + 1;
    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }))
  .sort((a, b) => b.value - a.value)
  .slice(0, 10);


const filteredDepartmentData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const department = record["Department"] || "Missing";
    acc[department] = (acc[department] || 0) + 1;
    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }))
  .sort((a, b) => b.value - a.value);


const filteredOperatorData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const operator = record["Operator"] || "Missing";
    acc[operator] = (acc[operator] || 0) + 1;
    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }))
  .sort((a, b) => b.value - a.value);


const filteredStatusData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const status = record["Status"] || "Missing";
    acc[status] = (acc[status] || 0) + 1;
    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }))
  .sort((a, b) => b.value - a.value);


const filteredClientData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const client = record["Client Y / N"] || "Missing";
    acc[client] = (acc[client] || 0) + 1;
    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }));

const filteredSolutionCategoryData = Object.entries(
  filteredRecords.reduce((acc, record) => {
    const solution = record["Solution Category"] || "Missing";

    acc[solution] = (acc[solution] || 0) + 1;

    return acc;
  }, {})
)
  .map(([name, value]) => ({ name, value }))
  .sort((a, b) => b.value - a.value);
  
  // Convert backend distribution object into chart data
  const complaintCategoryData = analysis
    ? Object.entries(analysis.complaint_category_distribution).map(
        ([name, value]) => ({
          name,
          value,
        })
      )
    : [];

  const departmentData = analysis
  ? Object.entries(analysis.department_distribution).map(
      ([name, value]) => ({
        name,
        value,
      })
    )
  : [];

  const statusData = analysis
  ? Object.entries(analysis.status_distribution).map(
      ([name, value]) => ({
        name,
        value,
      })
    )
  : [];

  const branchData = analysis
  ? Object.entries(analysis.branch_distribution)
      .map(([name, value]) => ({
        name,
        value,
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 10)
  : [];

const operatorData = analysis
  ? Object.entries(analysis.operator_distribution)
      .map(([name, value]) => ({
        name,
        value,
      }))
      .sort((a, b) => b.value - a.value)
  : [];

const clientData = analysis
  ? Object.entries(analysis.client_distribution).map(
      ([name, value]) => ({
        name,
        value,
      })
    )
  : [];

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>Trans Express Analytics</h1>
          <p>Customer Complaint & Operations Dashboard</p>
        </div>

        <div className="upload-area">
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
          />

          <button
            className="upload-button"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? "Analysing..." : "Analyse Dataset"}
          </button>
        </div>
      </header>

      {/* ERROR MESSAGE */}
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {/* DASHBOARD */}
      <main className="dashboard">
        {/* Filters */}
{analysis && (
  <section className="filter-section">

    <div className="filter-header">
      <div>
        <h2>Dashboard Filters</h2>
        <p>Filter the dashboard by branch, department, operator, status and client type.</p>
      </div>

      <button
        className="clear-filter-button"
        onClick={() => {
          setSelectedBranch("All");
          setSelectedDepartment("All");
          setSelectedOperator("All");
          setSelectedStatus("All");
          setSelectedClient("All");
        }}
      >
        Clear Filters
      </button>
    </div>

    <div className="filter-grid">

      {/* Branch */}
      <div className="filter-group">
        <label>Branch</label>

        <select
          value={selectedBranch}
          onChange={(e) => setSelectedBranch(e.target.value)}
        >
          <option value="All">All Branches</option>

          {branchOptions.map((branch) => (
            <option key={branch} value={branch}>
              {branch}
            </option>
          ))}
        </select>
      </div>


      {/* Department */}
      <div className="filter-group">
        <label>Department</label>

        <select
          value={selectedDepartment}
          onChange={(e) => setSelectedDepartment(e.target.value)}
        >
          <option value="All">All Departments</option>

          {departmentOptions.map((department) => (
            <option key={department} value={department}>
              {department}
            </option>
          ))}
        </select>
      </div>


      {/* Operator */}
      <div className="filter-group">
        <label>Operator</label>

        <select
          value={selectedOperator}
          onChange={(e) => setSelectedOperator(e.target.value)}
        >
          <option value="All">All Operators</option>

          {operatorOptions.map((operator) => (
            <option key={operator} value={operator}>
              {operator}
            </option>
          ))}
        </select>
      </div>


      {/* Status */}
      <div className="filter-group">
        <label>Status</label>

        <select
          value={selectedStatus}
          onChange={(e) => setSelectedStatus(e.target.value)}
        >
          <option value="All">All Statuses</option>

          {statusOptions.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>


      {/* Client */}
      <div className="filter-group">
        <label>Client Type</label>

        <select
          value={selectedClient}
          onChange={(e) => setSelectedClient(e.target.value)}
        >
          <option value="All">All</option>

          {clientOptions.map((client) => (
            <option key={client} value={client}>
              {client}
            </option>
          ))}
        </select>
      </div>

    </div>

  </section>
)}

  
        {/* KPI CARDS */}
        <section className="kpi-grid">

          <div className="kpi-card">
            <h3>Total Complaints</h3>
            <p>{analysis ? filteredTotalRecords : "-"}</p>
          </div>

          <div className="kpi-card">
            <h3>Branches</h3>
            <p>{analysis ? filteredBranches : "-"}</p>
          </div>

          <div className="kpi-card">
            <h3>Departments</h3>
            <p>{analysis ? filteredDepartments : "-"}</p>
          </div>

          <div className="kpi-card">
            <h3>Operators</h3>
            <p>{analysis ? filteredOperators : "-"}</p>
          </div>

        </section>

        {/* COMPLAINT CATEGORY CHART */}
        <section className="content-section">

          <div className="chart-card full-width">

            <h2>Complaint Categories</h2>

            {!analysis ? (
              <div className="placeholder">
                Upload and analyse a dataset to view the chart
              </div>
            ) : (
              <div className="chart-container">

                <ResponsiveContainer width="100%" height={400}>

                  <BarChart
                    data={complaintCategoryData}
                    layout="vertical"
                    margin={{
                      top: 20,
                      right: 30,
                      left: 30,
                      bottom: 20,
                    }}
                  >

                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                      type="number"
                    />

                    <YAxis
                       type="category"
                       dataKey="name"
                       width={180}
                    /> 

                    <Tooltip />

                    <Bar
                      dataKey="value"
                      name="Complaints"
                    />

                  </BarChart>

                </ResponsiveContainer>

              </div>
            )}

          </div>

        </section>

        {/* OTHER CHARTS - TEMPORARY */}
        <section className="content-section">

          <div className="chart-card">
  <h2>Department Distribution</h2>

  {!analysis ? (
    <div className="placeholder">
      Upload and analyse a dataset to view the chart
    </div>
  ) : (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={500}>
        <ScatterChart
          margin={{
            top: 20,
            right: 40,
            left: 20,
            bottom: 80,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            type="number"
            dataKey="index"
            domain={[0, departmentData.length - 1]}
            tickCount={departmentData.length}
            tickFormatter={(value) =>
              departmentData[value]?.name || ""
            }
            angle={-35}
            textAnchor="end"
            height={100}
            tick={{ fontSize: 11 }}
          />

          <YAxis
            type="number"
            dataKey="value"
            name="Complaints"
          />

          <Tooltip
            cursor={{ strokeDasharray: "3 3" }}
            formatter={(value) => [value, "Complaints"]}
            labelFormatter={(value) =>
              departmentData[value]?.name || ""
            }
          />

          <Scatter
            name="Departments"
            data={filteredDepartmentData.map((item, index) => ({
              ...item,
              index,
            }))}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )}
</div>

        </section>

        <section className="content-section">

          <div className="chart-card">
  <h2>Status Distribution</h2>

  {!analysis ? (
    <div className="placeholder">
      Upload and analyse a dataset to view the chart
    </div>
  ) : (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height={500}>
        <LineChart
          data={filteredStatusData}
          margin={{
            top: 20,
            right: 40,
            left: 20,
            bottom: 80,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />

          <XAxis
            dataKey="name"
            angle={-35}
            textAnchor="end"
            height={100}
            interval={0}
            tick={{ fontSize: 11 }}
          />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="value"
            name="Complaints"
            strokeWidth={3}
            dot={{ r: 5 }}
            activeDot={{ r: 7 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )}
</div>

        </section>

        <section className="content-section">

           {/* Branch Analysis */}
  <div className="chart-card">
    <h2>Top 10 Branches by Complaint Volume</h2>

    {!analysis ? (
      <div className="placeholder">
        Upload and analyse a dataset to view the chart
      </div>
    ) : (
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={450}>
          <BarChart
            data={filteredBranchData}
            layout="vertical"
            margin={{
              top: 20,
              right: 30,
              left: 20,
              bottom: 20,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis type="number" />

            <YAxis
              type="category"
              dataKey="name"
              width={130}
            />

            <Tooltip />

            <Bar
              dataKey="value"
              name="Complaints"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    )}
  </div>

  {/* Operator Workload */}
  <div className="chart-card">
    <h2>Operator Workload</h2>

    {!analysis ? (
      <div className="placeholder">
        Upload and analyse a dataset to view the chart
      </div>
    ) : (
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={450}>
          <BarChart
            data={filteredOperatorData}
            margin={{
              top: 20,
              right: 20,
              left: 10,
              bottom: 40,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis dataKey="name" />

            <YAxis />

            <Tooltip />

            <Bar
              dataKey="value"
              name="Complaints"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    )}
  </div>

</section>

  <section className="content-section">

  <div className="chart-card">
    <h2>Solution Categories</h2>

    {!analysis ? (
      <div className="placeholder">
        Upload and analyse a dataset to view the chart
      </div>
    ) : (
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={450}>
          <PieChart>
            <Pie
              data={filteredSolutionCategoryData}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={80}
              outerRadius={140}
              paddingAngle={2}
              label
            >
              {filteredSolutionCategoryData.map((entry, index) => (
                <Cell key={`solution-cell-${index}`} />
              ))}
            </Pie>

            <Tooltip />

            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    )}
  </div>

</section>
        
      </main>
    </div>
  );
}

export default App;