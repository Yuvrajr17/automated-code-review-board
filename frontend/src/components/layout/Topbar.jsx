
import { useEffect, useState } from "react";

function Topbar() {
  const [apiStatus, setApiStatus] = useState("checking");

  useEffect(() => {
    const checkAPI = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/health");

        if (!response.ok) {
          throw new Error("API is unavailable");
        }

        setApiStatus("online");
      } catch (error) {
        console.error("API health check failed:", error);
        setApiStatus("offline");
      }
    };

    checkAPI();
  }, []);

  const statusConfig = {
    checking: {
      label: "Checking API...",
      color: "bg-slate-400",
    },
    online: {
      label: "API Connected",
      color: "bg-emerald-500",
    },
    offline: {
      label: "API Offline",
      color: "bg-red-500",
    },
  };

  const currentStatus = statusConfig[apiStatus];

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-5 md:px-8">
      <div>
        <p className="text-sm font-semibold text-slate-800">
          Dashboard
        </p>
        <p className="text-xs text-slate-500">
          Automated Code Review
        </p>
      </div>

      <div className="flex items-center gap-2 rounded-full border border-slate-200 px-3 py-1.5">
        <span
          className={`h-2 w-2 rounded-full ${currentStatus.color}`}
        />
        <span className="text-xs font-medium text-slate-600">
          {currentStatus.label}
        </span>
      </div>
    </header>
  );
}

export default Topbar;
