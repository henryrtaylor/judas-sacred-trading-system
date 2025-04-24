import React from "react";
import SignalFeed from "@/components/SignalFeed";

const Dashboard = () => {
  return (
    <div className="p-4 space-y-6">
      <h1 className="text-3xl font-bold">📡 Judas Live Dashboard</h1>
      <div>
        <h2 className="text-xl font-semibold">⚡ Live Signal Feed</h2>
        <SignalFeed />
      </div>
    </div>
  );
};

export default Dashboard;
