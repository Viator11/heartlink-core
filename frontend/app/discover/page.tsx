'use client'
import { useEffect, useState } from 'react'
export default function Discover(){
  const [people,setPeople]=useState<any[]>([])
  useEffect(()=>{(async()=>{
    const t=localStorage.getItem('token')
    const r=await fetch((process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000')+'/matches/discover',{headers:{Authorization:`Bearer ${t}`}})
    setPeople(await r.json())
  })()},[])
  return <div><h2>Discover</h2><ul>{people.map((p:any)=><li key={p.id}>{p.display_name||'User'}</li>)}</ul></div>
}
