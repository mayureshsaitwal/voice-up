import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card"
import { CheckCircle, XCircle } from "lucide-react"
import { useEffect, useState } from "react"
import axios from "axios"

const emojiMap: Record<string, string> = {
  happy: "😊",
  neutral: "😐",
  angry: "😠",
}

type AnalysisRow = {
  conversation_id: number
  customer_name: string
  emotion_summary: {
    angry: number
    neutral: number
    happy: number
  }
  compliance_summary: {
    rule_1: boolean
    rule_2: boolean
    rule_3: boolean
    rule_4: boolean
    rule_5: boolean
  }
}

export default function AnalysisTable() {
  const [data, setData] = useState<AnalysisRow[]>([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const { data } = await axios.get<AnalysisRow[]>("http://127.0.0.1:8000/api/stats/analysis-table/")
        console.log(data)
        setData(data)
      } catch (err) {
        console.error("Failed to fetch analysis table", err)
      }
    }

    fetchData()
  }, [])

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Conversation Analysis</CardTitle>
        <CardDescription>Includes emotion and compliance breakdowns</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Conversation ID</TableHead>
              <TableHead>Customer</TableHead>
              <TableHead>Emotion Summary</TableHead>
              <TableHead>Compliance Summary</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                <TableCell>{row.conversation_id}</TableCell>
                <TableCell>{row.customer_name}</TableCell>
                <TableCell className="whitespace-nowrap">
                  {Object.entries(row.emotion_summary).map(([emotion, count]) => (
                    <div key={emotion} className="flex items-center gap-1">
                      <span>{emojiMap[emotion]}</span>
                      <span>{count}</span>
                    </div>
                  ))}
                </TableCell>
                <TableCell>
                  {Object.entries(row.compliance_summary).map(([_rule, passed], i) => (
                    <div key={i} className="flex items-center gap-2">
                      <span>Rule {i + 1}:</span>
                      {passed ? (
                        <span className="text-green-600 flex items-center gap-1">
                          <CheckCircle className="h-4 w-4" /> Pass
                        </span>
                      ) : (
                        <span className="text-red-600 flex items-center gap-1">
                          <XCircle className="h-4 w-4" /> Fail
                        </span>
                      )}
                    </div>
                  ))}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
