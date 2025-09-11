import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Download, FileText, Calendar } from "lucide-react"

const reports = [
  {
    id: 1,
    title: "Weekly Assignment 5",
    description: "Dynamic Programming",
    date: "2024-01-15",
    size: "2.4 MB",
    format: "Excel",
  },
  {
    id: 2,
    title: "Assignment 4",
    description: "Greedy Algorithms",
    date: "2024-01-14",
    size: "1.8 MB",
    format: "Excel",
  },
  {
    id: 3,
    title: "Project Assignments 1",
    description: " array manipulation and sorting",
    date: "2024-01-10",
    size: "3.2 MB",
    format: "Excel",
  },
  {
    id: 4,
    title: "Assignment 3",
    description: "linked lists and trees",
    date: "2024-01-08",
    size: "1.5 MB",
    format: "Excel",
  }
]

export function ReportsContent() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Downloadable Reports</h2>
        <Button variant="outline">
          <Calendar className="h-4 w-4 mr-2" />
          Filter by Date
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((report) => (
          <Card key={report.id} className="hover:shadow-md transition-shadow">
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <FileText className="h-8 w-8 text-accent" />
                <span className="text-xs bg-muted px-2 py-1 rounded">{report.format}</span>
              </div>
              <CardTitle className="text-lg">{report.title}</CardTitle>
              <CardDescription className="text-sm">{report.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between text-sm text-muted-foreground mb-4">
                <span>{report.date}</span>
                <span>{report.size}</span>
              </div>
              <Button className="w-full" size="sm">
                <Download className="h-4 w-4 mr-2" />
                Download
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
