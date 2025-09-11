"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Bar, BarChart, Line, LineChart, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const submissionData = [
  { assignment: "Assignment 1", submissions: 58, detections: 12 },
  { assignment: "Assignment 2", submissions: 60, detections: 8 },
  { assignment: "Assignment 3", submissions: 57, detections: 15 },
  { assignment: "Assignment 4", submissions: 59, detections: 6 },
]

const similarityData = [
  { assignment: "Assignment 1", avgSimilarity: 23.5 },
  { assignment: "Assignment 2", avgSimilarity: 18.2 },
  { assignment: "Assignment 3", avgSimilarity: 31.8 },
  { assignment: "Assignment 4", avgSimilarity: 15.4 },
]

export function DashboardContent() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Total Submissions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">234</div>
            <p className="text-xs text-muted-foreground">+3.5% from Assignment 3</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Students Scanned</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">60/60</div>
            <p className="text-xs text-muted-foreground">100% coverage rate</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Flagged Cases</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">41</div>
            <p className="text-xs text-muted-foreground">17.5% detection rate</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium">Avg Similarity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">22.2%</div>
            <p className="text-xs text-muted-foreground">-2.8% from last assignment</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Submissions & Detections</CardTitle>
            <CardDescription>Assignment-based submission and detection data</CardDescription>
          </CardHeader>
          <CardContent className="px-2 sm:px-6">
            <ChartContainer
              config={{
                submissions: {
                  label: "Submissions",
                  color: "hsl(var(--chart-1))",
                },
                detections: {
                  label: "Detections",
                  color: "hsl(var(--chart-2))",
                },
              }}
              className="h-[300px] w-full"
            >
              <ResponsiveContainer width="99%" height="100%">
                <BarChart data={submissionData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="assignment" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Bar dataKey="submissions" fill="var(--color-chart-1)" />
                  <Bar dataKey="detections" fill="var(--color-chart-2)" />
                </BarChart>
              </ResponsiveContainer>
            </ChartContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Similarity Distribution</CardTitle>
            <CardDescription>Average similarity percentage across assignments</CardDescription>
          </CardHeader>
          <CardContent className="px-2 sm:px-6">
            <ChartContainer
              config={{
                avgSimilarity: {
                  label: "Avg Similarity %",
                  color: "hsl(var(--chart-3))",
                },
              }}
              className="h-[300px] w-full"
            >
              <ResponsiveContainer width="99%" height="100%">
                <LineChart data={similarityData} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="assignment" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <ChartTooltip content={<ChartTooltipContent />} />
                  <Line type="monotone" dataKey="avgSimilarity" stroke="var(--color-chart-3)" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </ChartContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
