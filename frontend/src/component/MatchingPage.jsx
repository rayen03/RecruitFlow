import React from 'react'
import FileInput from './FileInput'
import JobInput from './JobInput'
import { Link } from 'react-router-dom'

const MatchingPage = () => {
  return (
    <div className='main flex-col h-screen w-full'>
      <Link to='/' className='normal_header_text pl-2'>Recruit<span className='blue_gradient'>Flow</span></Link>
      <div className='flex h-full '>
        <div className='flex flex-col pl-6  mt-6 gap-6 w-[50%] '>
        <h1 className='normal_header_text'>Upload Your Candidates Resumes Here:</h1>
        <FileInput/>
        </div>
        <div className='flex flex-col  mt-6 gap-6 w-[50%] '>
          <JobInput />
        </div>
        
      </div>
      </div>
  )
}

export default MatchingPage