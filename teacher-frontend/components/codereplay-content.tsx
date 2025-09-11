"use client"

import { useState, useEffect, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Play, Pause, RotateCcw, GitCompare, X, Search } from "lucide-react"

interface KeystrokeEvent {
  timestamp: number
  type: "insert" | "delete" | "backspace"
  position: number
  content: string
}

// John Doe's Python code - factorial function
const sampleKeystrokeLog1: KeystrokeEvent[] = [
  { timestamp: 0, type: "insert", position: 0, content: "def" },
  { timestamp: 200, type: "insert", position: 3, content: " " },
  { timestamp: 400, type: "insert", position: 4, content: "factorial" },
  { timestamp: 800, type: "insert", position: 13, content: "(" },
  { timestamp: 900, type: "insert", position: 14, content: "n" },
  { timestamp: 1000, type: "insert", position: 15, content: ")" },
  { timestamp: 1100, type: "insert", position: 16, content: ":" },
  { timestamp: 1300, type: "insert", position: 17, content: "\n    " },
  { timestamp: 1500, type: "insert", position: 22, content: "if" },
  { timestamp: 1700, type: "insert", position: 24, content: " " },
  { timestamp: 1800, type: "insert", position: 25, content: "n" },
  { timestamp: 1900, type: "insert", position: 26, content: " " },
  { timestamp: 2000, type: "insert", position: 27, content: "<=" },
  { timestamp: 2200, type: "insert", position: 29, content: " " },
  { timestamp: 2300, type: "insert", position: 30, content: "1" },
  { timestamp: 2400, type: "insert", position: 31, content: ":" },
  { timestamp: 2600, type: "insert", position: 32, content: "\n        " },
  { timestamp: 2800, type: "insert", position: 40, content: "return" },
  { timestamp: 3200, type: "insert", position: 46, content: " " },
  { timestamp: 3300, type: "insert", position: 47, content: "1" },
  { timestamp: 3500, type: "insert", position: 48, content: "\n    " },
  { timestamp: 3700, type: "insert", position: 53, content: "else" },
  { timestamp: 4000, type: "insert", position: 57, content: ":" },
  { timestamp: 4200, type: "insert", position: 58, content: "\n        " },
  { timestamp: 4400, type: "insert", position: 66, content: "return" },
  { timestamp: 4800, type: "insert", position: 72, content: " " },
  { timestamp: 4900, type: "insert", position: 73, content: "n" },
  { timestamp: 5000, type: "insert", position: 74, content: " " },
  { timestamp: 5100, type: "insert", position: 75, content: "*" },
  { timestamp: 5200, type: "insert", position: 76, content: " " },
  { timestamp: 5300, type: "insert", position: 77, content: "factorial" },
  { timestamp: 5700, type: "insert", position: 86, content: "(" },
  { timestamp: 5800, type: "insert", position: 87, content: "n" },
  { timestamp: 5900, type: "insert", position: 88, content: " " },
  { timestamp: 6000, type: "insert", position: 89, content: "-" },
  { timestamp: 6100, type: "insert", position: 90, content: " " },
  { timestamp: 6200, type: "insert", position: 91, content: "1" },
  { timestamp: 6300, type: "insert", position: 92, content: ")" }
]

// Jane Smith's Python code - similar factorial function with slight differences
const sampleKeystrokeLog2: KeystrokeEvent[] = [
  { timestamp: 0, type: "insert", position: 0, content: "def" },
  { timestamp: 250, type: "insert", position: 3, content: " " },
  { timestamp: 500, type: "insert", position: 4, content: "calculate_factorial" },
  { timestamp: 1200, type: "insert", position: 22, content: "(" },
  { timestamp: 1350, type: "insert", position: 23, content: "num" },
  { timestamp: 1650, type: "insert", position: 26, content: ")" },
  { timestamp: 1800, type: "insert", position: 27, content: ":" },
  { timestamp: 2000, type: "insert", position: 28, content: "\n    " },
  { timestamp: 2200, type: "insert", position: 33, content: "if" },
  { timestamp: 2400, type: "insert", position: 35, content: " " },
  { timestamp: 2500, type: "insert", position: 36, content: "num" },
  { timestamp: 2800, type: "insert", position: 39, content: " " },
  { timestamp: 2900, type: "insert", position: 40, content: "<=" },
  { timestamp: 3100, type: "insert", position: 42, content: " " },
  { timestamp: 3200, type: "insert", position: 43, content: "1" },
  { timestamp: 3300, type: "insert", position: 44, content: ":" },
  { timestamp: 3500, type: "insert", position: 45, content: "\n        " },
  { timestamp: 3700, type: "insert", position: 53, content: "return" },
  { timestamp: 4100, type: "insert", position: 59, content: " " },
  { timestamp: 4200, type: "insert", position: 60, content: "1" },
  { timestamp: 4400, type: "insert", position: 61, content: "\n    " },
  { timestamp: 4600, type: "insert", position: 66, content: "else" },
  { timestamp: 4900, type: "insert", position: 70, content: ":" },
  { timestamp: 5100, type: "insert", position: 71, content: "\n        " },
  { timestamp: 5300, type: "insert", position: 79, content: "return" },
  { timestamp: 5700, type: "insert", position: 85, content: " " },
  { timestamp: 5800, type: "insert", position: 86, content: "num" },
  { timestamp: 6100, type: "insert", position: 89, content: " " },
  { timestamp: 6200, type: "insert", position: 90, content: "*" },
  { timestamp: 6300, type: "insert", position: 91, content: " " },
  { timestamp: 6400, type: "insert", position: 92, content: "calculate_factorial" },
  { timestamp: 7200, type: "insert", position: 110, content: "(" },
  { timestamp: 7300, type: "insert", position: 111, content: "num" },
  { timestamp: 7600, type: "insert", position: 114, content: " " },
  { timestamp: 7700, type: "insert", position: 115, content: "-" },
  { timestamp: 7800, type: "insert", position: 116, content: " " },
  { timestamp: 7900, type: "insert", position: 117, content: "1" },
  { timestamp: 8000, type: "insert", position: 118, content: ")" }
]

// Alice's Python code - different approach with loop
const sampleKeystrokeLog3: KeystrokeEvent[] = [
  { timestamp: 0, type: "insert", position: 0, content: "def" },
  { timestamp: 300, type: "insert", position: 3, content: " " },
  { timestamp: 600, type: "insert", position: 4, content: "power" },
  { timestamp: 1100, type: "insert", position: 9, content: "(" },
  { timestamp: 1200, type: "insert", position: 10, content: "base" },
  { timestamp: 1600, type: "insert", position: 14, content: "," },
  { timestamp: 1700, type: "insert", position: 15, content: " " },
  { timestamp: 1800, type: "insert", position: 16, content: "exp" },
  { timestamp: 2100, type: "insert", position: 19, content: ")" },
  { timestamp: 2200, type: "insert", position: 20, content: ":" },
  { timestamp: 2400, type: "insert", position: 21, content: "\n    " },
  { timestamp: 2600, type: "insert", position: 26, content: "result" },
  { timestamp: 3200, type: "insert", position: 32, content: " " },
  { timestamp: 3300, type: "insert", position: 33, content: "=" },
  { timestamp: 3400, type: "insert", position: 34, content: " " },
  { timestamp: 3500, type: "insert", position: 35, content: "1" },
  { timestamp: 3700, type: "insert", position: 36, content: "\n    " },
  { timestamp: 3900, type: "insert", position: 41, content: "for" },
  { timestamp: 4200, type: "insert", position: 44, content: " " },
  { timestamp: 4300, type: "insert", position: 45, content: "i" },
  { timestamp: 4400, type: "insert", position: 46, content: " " },
  { timestamp: 4500, type: "insert", position: 47, content: "in" },
  { timestamp: 4700, type: "insert", position: 49, content: " " },
  { timestamp: 4800, type: "insert", position: 50, content: "range" },
  { timestamp: 5300, type: "insert", position: 55, content: "(" },
  { timestamp: 5400, type: "insert", position: 56, content: "exp" },
  { timestamp: 5700, type: "insert", position: 59, content: ")" },
  { timestamp: 5800, type: "insert", position: 60, content: ":" },
  { timestamp: 6000, type: "insert", position: 61, content: "\n        " },
  { timestamp: 6200, type: "insert", position: 69, content: "result" },
  { timestamp: 6800, type: "insert", position: 75, content: " " },
  { timestamp: 6900, type: "insert", position: 76, content: "*=" },
  { timestamp: 7100, type: "insert", position: 78, content: " " },
  { timestamp: 7200, type: "insert", position: 79, content: "base" },
  { timestamp: 7600, type: "insert", position: 83, content: "\n    " },
  { timestamp: 7800, type: "insert", position: 88, content: "return" },
  { timestamp: 8200, type: "insert", position: 94, content: " " },
  { timestamp: 8300, type: "insert", position: 95, content: "result" }
]

export default function CodeReplayContent() {
  const [isCompareMode, setIsCompareMode] = useState(false)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentEventIndex, setCurrentEventIndex] = useState(0)
  const [codeContent, setCodeContent] = useState("")
  const [compareCodeContent, setCompareCodeContent] = useState("")
  const [speed, setSpeed] = useState(3)

  const [selectedAssignment, setSelectedAssignment] = useState("Assignment 1")
  const [studentSearchQuery, setStudentSearchQuery] = useState("")
  const [selectedStudent, setSelectedStudent] = useState("")
  const [compareStudentSearchQuery, setCompareStudentSearchQuery] = useState("")
  const [compareSelectedStudent, setCompareSelectedStudent] = useState("")
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [showCompareSuggestions, setShowCompareSuggestions] = useState(false)

  const intervalRef = useRef<NodeJS.Timeout>()
  const compareIntervalRef = useRef<NodeJS.Timeout>()

  const assignments = ["Assignment 1", "Assignment 2", "Assignment 3", "Assignment 4"]

  const studentsData = {
    "John Doe": sampleKeystrokeLog1,
    "Jane Smith": sampleKeystrokeLog2,
    "Alice Johnson": sampleKeystrokeLog3,
    "Bob Wilson": sampleKeystrokeLog2,
    "Mike Brown": sampleKeystrokeLog1,
    "Sarah Davis": sampleKeystrokeLog3,
  }

  const allStudents = Object.keys(studentsData)

  const getFilteredStudents = (searchQuery: string) => {
    return allStudents.filter((student) => student.toLowerCase().includes(searchQuery.toLowerCase()))
  }

  // Typing animation function based on your provided code
  const animateTyping = (targetContent: string, isCompare = false) => {
    let i = 0
    const content = targetContent
    
    if (isCompare) {
      setCompareCodeContent("")
      clearInterval(compareIntervalRef.current)
      compareIntervalRef.current = setInterval(() => {
        if (i < content.length) {
          setCompareCodeContent(prev => prev + content[i])
          i++
        } else {
          clearInterval(compareIntervalRef.current!)
        }
      }, 1000 / (speed * 10)) // Adjust speed for smoother animation
    } else {
      setCodeContent("")
      clearInterval(intervalRef.current)
      intervalRef.current = setInterval(() => {
        if (i < content.length) {
          setCodeContent(prev => prev + content[i])
          i++
        } else {
          clearInterval(intervalRef.current!)
          setIsPlaying(false)
        }
      }, 1000 / (speed * 10))
    }
  }

  const applyKeystrokeEvent = (event: KeystrokeEvent, content: string): string => {
    switch (event.type) {
      case "insert":
        return content.slice(0, event.position) + event.content + content.slice(event.position)
      case "delete":
        return content.slice(0, event.position) + content.slice(event.position + 1)
      case "backspace":
        return content.slice(0, Math.max(0, event.position - 1)) + content.slice(event.position)
      default:
        return content
    }
  }

  const playReplay = () => {
    const selectedLog = studentsData[selectedStudent as keyof typeof studentsData]
    const compareLog = studentsData[compareSelectedStudent as keyof typeof studentsData]

    if (!selectedLog || (isCompareMode && !compareLog)) return

    setIsPlaying(true)
    setCurrentEventIndex(0)
    setCodeContent("")
    setCompareCodeContent("")

    // Build the final content from keystroke events
    let finalContent = ""
    let compareFinalContent = ""

    selectedLog.forEach(event => {
      finalContent = applyKeystrokeEvent(event, finalContent)
    })

    if (isCompareMode && compareLog) {
      compareLog.forEach(event => {
        compareFinalContent = applyKeystrokeEvent(event, compareFinalContent)
      })
    }

    // Start typing animations
    animateTyping(finalContent, false)
    if (isCompareMode && compareLog) {
      animateTyping(compareFinalContent, true)
    }

    // Update progress
    const updateProgress = () => {
      const progressInterval = setInterval(() => {
        if (!isPlaying) {
          clearInterval(progressInterval)
          return
        }
        
        setCurrentEventIndex(prev => {
          const newIndex = Math.min(prev + 1, selectedLog.length)
          if (newIndex >= selectedLog.length) {
            clearInterval(progressInterval)
          }
          return newIndex
        })
      }, (8000 / speed) / selectedLog.length) // Distribute progress over animation time
    }
    
    updateProgress()
  }

  const pauseReplay = () => {
    setIsPlaying(false)
    clearInterval(intervalRef.current)
    clearInterval(compareIntervalRef.current)
  }

  const resetReplay = () => {
    setIsPlaying(false)
    setCurrentEventIndex(0)
    setCodeContent("")
    setCompareCodeContent("")
    clearInterval(intervalRef.current)
    clearInterval(compareIntervalRef.current)
  }

  const toggleCompareMode = () => {
    setIsCompareMode(!isCompareMode)
    if (!isCompareMode) {
      setCompareCodeContent("")
      setCompareSelectedStudent("")
      setCompareStudentSearchQuery("")
    }
  }

  useEffect(() => {
    return () => {
      clearInterval(intervalRef.current)
      clearInterval(compareIntervalRef.current)
    }
  }, [])

  return (
    <div className="space-y-6">
      {/* Assignment Selection and Speed */}
      <div className="flex items-center space-x-4">
        <Select value={selectedAssignment} onValueChange={setSelectedAssignment}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Select Assignment" />
          </SelectTrigger>
          <SelectContent>
            {assignments.map((assignment) => (
              <SelectItem key={assignment} value={assignment}>
                {assignment}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        
        <div className="flex items-center space-x-2">
          <span className="text-sm text-muted-foreground">Speed:</span>
          <Select value={speed.toString()} onValueChange={(value) => setSpeed(Number(value))}>
            <SelectTrigger className="w-20">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1">1x</SelectItem>
              <SelectItem value="2">2x</SelectItem>
              <SelectItem value="3">3x</SelectItem>
              <SelectItem value="5">5x</SelectItem>
              <SelectItem value="10">10x</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={isPlaying ? pauseReplay : playReplay}
            disabled={!selectedStudent || (isCompareMode && !compareSelectedStudent)}
          >
            {isPlaying ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            {isPlaying ? "Pause" : "Play"}
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={resetReplay}
            disabled={!selectedStudent || (isCompareMode && !compareSelectedStudent)}
          >
            <RotateCcw className="h-4 w-4" />
            Reset
          </Button>

          <Button variant="outline" size="sm" onClick={toggleCompareMode} disabled={!selectedStudent}>
            <GitCompare className="h-4 w-4" />
            Compare
          </Button>
        </div>

        {/* Header with Compare Mode Toggle */}
        {isCompareMode && (
          <Button
            variant="ghost"
            size="sm"
            onClick={toggleCompareMode}
            className="text-muted-foreground hover:text-foreground"
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Search Bar */}
      <div className="flex items-center justify-between space-x-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
          <Input
            placeholder="Search students..."
            value={studentSearchQuery}
            onChange={(e) => {
              setStudentSearchQuery(e.target.value)
              setShowSuggestions(true)
            }}
            onFocus={() => setShowSuggestions(true)}
            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
            className="pl-10 w-64"
          />
          {showSuggestions && studentSearchQuery && (
            <div className="absolute top-full left-0 right-0 bg-background border rounded-md shadow-lg z-10 max-h-40 overflow-y-auto">
              {getFilteredStudents(studentSearchQuery).map((student) => (
                <div
                  key={student}
                  className="px-3 py-2 hover:bg-muted cursor-pointer text-sm"
                  onClick={() => {
                    setSelectedStudent(student)
                    setStudentSearchQuery(student)
                    setShowSuggestions(false)
                  }}
                >
                  {student}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Compare Mode Search */}
        {isCompareMode && (
          <div className="relative w-64">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
            <Input
              placeholder="Search students to compare..."
              value={compareStudentSearchQuery}
              onChange={(e) => {
                setCompareStudentSearchQuery(e.target.value)
                setShowCompareSuggestions(true)
              }}
              onFocus={() => setShowCompareSuggestions(true)}
              onBlur={() => setTimeout(() => setShowCompareSuggestions(false), 200)}
              className="pl-10"
            />
            {showCompareSuggestions && compareStudentSearchQuery && (
              <div className="absolute top-full left-0 right-0 bg-background border rounded-md shadow-lg z-10 max-h-40 overflow-y-auto">
                {getFilteredStudents(compareStudentSearchQuery).map((student) => (
                  <div
                    key={student}
                    className="px-3 py-2 hover:bg-muted cursor-pointer text-sm"
                    onClick={() => {
                      setCompareSelectedStudent(student)
                      setCompareStudentSearchQuery(student)
                      setShowCompareSuggestions(false)
                    }}
                  >
                    {student}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Main Content Area */}
      <div
        className={`transition-all duration-500 ease-in-out ${
          isCompareMode ? "grid grid-cols-2 gap-6" : "grid grid-cols-1"
        }`}
      >
        <div className="border rounded-lg overflow-hidden">
          <div className="bg-slate-800 text-white px-4 py-2 border-b flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="flex space-x-1">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              <span className="text-sm font-medium ml-2">
                {selectedStudent ? `${selectedStudent}.py` : "Select Student"}
              </span>
            </div>
            {isPlaying && <span className="animate-pulse text-green-400">●</span>}
          </div>
          <div className="bg-slate-900 text-green-400 p-4 h-96 overflow-auto font-mono text-sm">
            <div className="whitespace-pre-wrap">
              {codeContent ||
                (selectedStudent
                  ? "# Click play to start replay..."
                  : "# Select a student to view their code replay")}
              {isPlaying && <span className="animate-pulse text-white">|</span>}
            </div>
          </div>
        </div>

        {/* Comparison View */}
        {isCompareMode && (
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-slate-800 text-white px-4 py-2 border-b flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                </div>
                <span className="text-sm font-medium ml-2">
                  {compareSelectedStudent ? `${compareSelectedStudent}.py` : "Select Student to Compare"}
                </span>
              </div>
              {isPlaying && compareSelectedStudent && <span className="animate-pulse text-green-400">●</span>}
            </div>
            <div className="bg-slate-900 text-green-400 p-4 h-96 overflow-auto font-mono text-sm">
              <div className="whitespace-pre-wrap">
                {compareCodeContent ||
                  (compareSelectedStudent ? "# Click play to start replay..." : "# Select a student to compare")}
                {isPlaying && compareSelectedStudent && <span className="animate-pulse text-white">|</span>}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}