import { Card, CardHeader, CardContent, CardTitle, CardDescription } from "@/components/ui/card"

type StatCardProps = {
  label: string
  value: string | number
  change: string
}

export default function StatCard({ label, value, change }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardDescription>{label}</CardDescription>
        <CardTitle className="text-4xl">{value}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-xs text-muted-foreground">{change}</div>
      </CardContent>
    </Card>
  )
}

