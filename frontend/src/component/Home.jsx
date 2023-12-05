import React from 'react'
import scan from '../assets/task-searching.png'
import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className='main flex flex-col items-center gap-16 w-full'>
        <h1 className='head_text'>Recruit<span className='blue_gradient'>Flow</span></h1>
        <img
            className=' h-80 w-80 z-1' 
            src={scan} alt="" />
        <div className='flex-center gap-32 w-full '>
            <Link to="/matchingpage" className='cyan_btn w-56 h-12'>
                Start Matching
            </Link>
        
        </div>
        
        
    </div>
  )
}

export default Home