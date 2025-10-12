'use client'
import { useEffect, useState } from 'react'
export default function Profile(){
  const [profile,setProfile]=useState<any>(null)
  useEffect(()=>{(async()=>{
    const t=localStorage.getItem('token')
    const r=await fetch((process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000')+'/profiles/me',{headers:{Authorization:`Bearer ${t}`}})
    setProfile(await r.json())
  })()},[])
  if(!profile) return <p>Loading…</p>
  return <div><h2>{profile?.display_name||'My profile'}</h2><p>{profile?.bio||'No bio yet.'}</p></div>
}
