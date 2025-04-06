import React, { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";

const mockPortfolio = [
  { symbol: "NVDA", actual: 0.12, target: 0.20 },
  { symbol: "QQQ", actual: 0.25, target: 0.25 },
  { symbol: "SCHD", actual: 0.18, target: 0.30 },
  { symbol: "JEPI", actual: 0.15, target: 0.10 },
  { symbol: "CASH", actual: 0.30, target: 0.15 }
];

export default function DashboardGUI() {
  const [portfolio, setPortfolio] = useState([]);

  useEffect(() => {
    // In production: fetch from backend or load live
    setPortfolio(mockPortfolio);
  }, []);

  const getDeltaColor = (delta) => {
    if (Math.abs(delta) < 0.01) return "bg-green-500";
    return delta > 0 ? "bg-red-500" : "bg-yellow-500";
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">📊 Portfolio Alignment Dashboard</h1>
      <ScrollArea className="h-[500px] pr-2">
        <div className="space-y-4">
          {portfolio.map(({ symbol, actual, target }) => {
            const delta = actual - target;
            const deltaPct = (delta * 100).toFixed(2);
            return (
              <Card key={symbol} className="shadow-md">
                <CardContent className="p-4">
                  <div className="flex justify-between items-center mb-2">
                    <h2 className="text-lg font-semibold">{symbol}</h2>
                    <Badge className={getDeltaColor(delta)}>
                      Drift: {deltaPct}%
                    </Badge>
                  </div>
                  <div className="mb-1 text-sm">Target: {(target * 100).toFixed(1)}%</div>
                  <Progress value={actual * 100} className="h-4" />
                  <div className="text-right text-xs mt-1 text-muted-foreground">
                    Current: {(actual * 100).toFixed(1)}%
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}
