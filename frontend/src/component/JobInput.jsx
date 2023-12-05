import React from 'react'

const JobInput = () => {
  return (
    <div className='h-full flex flex-col '>
      <div className='flex flex-col gap-4  '>
        <h1 className='normal_header_text'>Write The job description</h1>
      <textarea
      className='w-[400px] border-dashed border-[2px] border-cyan-800 h-[400px] rounded-lg p-4 outline-none resize-none'
      placeholder='The Job description'/>

      <button className='w-[15%] h-12 cyan_btn ml-32' >
        MATCH!
      </button>
      </div>
      
    </div>
  )
}

export default JobInput