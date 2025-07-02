import { useEffect, useState } from "react"
import axios from "axios"
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@/components/ui/separator"
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from "@/components/ui/card"
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid, LineChart, Line } from "recharts"
import {
  ChartTooltip,
} from "@/components/ui/chart"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const COLORS = ["#4ade80", "#f87171", "#facc15"]

type EmotionItem = { name: string; value: number }
type CoversationTableItem = { customer_name: string; emotion: string }
type ComplianceItem = { conversation_id: number; compliance_scores: string }
type ComplianceTrendItem = { id: number; score: number }
type EmotionTrendItem = { id: number; emotion: number }

export default function Dashboard() {
  const [emotionData, setEmotionData] = useState<EmotionItem[]>([])
  const [conversationTable, setConversationTable] = useState<CoversationTableItem[]>([])
  const [complianceScores, setComplianceScores] = useState<ComplianceItem[]>([])
  const [totalConversations, setTotalConversations] = useState(0)
  const [loading, setLoading] = useState(false)
  const [complianceTrend, setComplianceTrend] = useState<ComplianceTrendItem[]>([])
  const [emotionTrend, setEmotionTrend] = useState<EmotionTrendItem[]>([])
  const [selectedEmotion, setSelectedEmotion] = useState<string>("all")

  const emotionMap = {
    happy: 2,
    neutral: 1,
    angry: 0,
  }

  const reverseEmotionMap: Record<number, string> = {
    0: 'Angry',
    1: 'Neutral',
    2: 'Happy',
  }


  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      try {
        const [
          conversationRes,
          emotionRes,
          tableRes,
          complianceScoresRes,
          complianceTrendRes,
        ] = await Promise.all([
          axios.get("http://127.0.0.1:8000/api/stats/conversations/"),
          axios.get("http://127.0.0.1:8000/api/stats/emotions/"),
          axios.get("http://127.0.0.1:8000/api/stats/emotion-table/"),
          axios.get("http://127.0.0.1:8000/api/stats/compliance-scores/"),
          axios.get("http://127.0.0.1:8000/api/stats/compliance-trend/"),
        ]);

        setTotalConversations(conversationRes.data.total);

        const formattedEmotions = emotionRes.data.map((item: { emotion: string; count: number }) => ({
          name: item.emotion,
          value: item.count,
        }));
        setEmotionData(formattedEmotions);

        setConversationTable(tableRes.data);

        const formattedEmotionTrend: EmotionTrendItem[] = tableRes.data.map(
          (item: { conversation_id: number; emotion: string }) => ({
            id: item.conversation_id,
            emotion: emotionMap[item.emotion.toLowerCase() as keyof typeof emotionMap],
          })
        );
        setEmotionTrend(formattedEmotionTrend);

        const formattedComplianceScores = complianceScoresRes.data.map((item: { compliance_score: number; count: number }) => ({
          name: item.compliance_score.toString(),
          value: item.count,
        }));
        setComplianceScores(formattedComplianceScores);

        const formattedComplianceTrend = complianceTrendRes.data.map((item: { conversation_id: number; compliance_score: number }) => ({
          id: item.conversation_id,
          score: item.compliance_score,
        }));
        setComplianceTrend(formattedComplianceTrend);

      } catch (error: any) {
        console.error("Error fetching dashboard data:", error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);


  console.log("Emotion:", emotionTrend)

  if (!loading) {
    return (
      <SidebarInset>
        <header className="flex h-16 items-center gap-2">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <h1 className="text-lg font-semibold">Home</h1>
          </div>
        </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Emotion Summary</CardTitle>
                <CardDescription>Breakdown of customer emotions</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <PieChart width={300} height={200}>
                  <Pie data={emotionData} dataKey="value" nameKey="name" outerRadius={80}>
                    {emotionData.map((_entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardHeader>
                <CardTitle>Compliance Score Distribution</CardTitle>
                <CardDescription>Grouped compliance scores by range</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <BarChart width={300} height={200} data={complianceScores}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="#6366f1" />
                </BarChart>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardHeader>
                <CardTitle>Total Conversations</CardTitle>
                <CardDescription>Overall tracked sessions</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center items-center h-full">
                <div className="text-7xl font-bold">{totalConversations}</div>
              </CardContent>
            </Card>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <Card className="w-full">
              <CardHeader>
                <CardTitle>Compliance Trend</CardTitle>
                <CardDescription>Time series trend of scores</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={complianceTrend}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="id" label={{ value: "Conversation ID", position: "insideBottom", offset: -5 }} />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="score" stroke="#6366f1" name="Compliance Score" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card className="w-full">
              <CardHeader>
                <CardTitle>Emotion Trend</CardTitle>
                <CardDescription>Time Series trend for emotions</CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart
                    accessibilityLayer
                    data={emotionTrend}
                    margin={{
                      left: 12,
                      right: 12,
                    }}
                  >
                    <CartesianGrid vertical={false} />
                    <XAxis
                      dataKey="id"
                      tickLine={true}
                      axisLine={true}
                      tickMargin={8}
                    />
                    <YAxis
                      domain={[-1, 3]}
                      ticks={[0, 1, 2]}
                      tickFormatter={(tick: number) => reverseEmotionMap[tick]}
                      tickLine={true}
                      axisLine={true}
                      tickMargin={8}
                    />
                    <ChartTooltip
                      cursor={true}
                      content={({ payload }) => {
                        const value = payload?.[0]?.value;
                        const label = reverseEmotionMap[value];
                        return (
                          <div style={{ background: 'white', padding: 8, borderRadius: 4, boxShadow: '0 0 4px rgba(0,0,0,0.15)' }}>
                            <strong>{label ?? "Unknown"}</strong>
                          </div>
                        );
                      }}
                    />
                    <Line
                      dataKey="emotion"
                      type="linear"
                      stroke="#6366f1"
                      strokeWidth={2}
                      dot={true}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          <div className="w-full max-w-4xl">
            <div className="flex items-center justify-center px-4 py-3 border-b">
              <h2 className="text-lg font-semibold mr-3">Emotion:</h2>
              <select
                className="border border-gray-300 rounded px-2 py-1 text-sm"
                value={selectedEmotion}
                onChange={(e) => setSelectedEmotion(e.target.value)}
              >
                <option value="all">All</option>
                <option value="happy">Happy</option>
                <option value="neutral">Neutral</option>
                <option value="angry">Angry</option>
              </select>
            </div>
          </div>
          <Card className="w-full max-w-4xl">
            <CardHeader>
              <CardTitle>Customer Table</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Customer Table</TableHead>
                    <TableHead>Emotion</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {conversationTable
                    .filter(row => selectedEmotion === "all" || row.emotion === selectedEmotion)
                    .map((row, index) => (
                      <TableRow key={index}>
                        <TableCell className="items-center">{row.customer_name}</TableCell>
                        <TableCell>{row.emotion}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </SidebarInset>
    )
  }
}

