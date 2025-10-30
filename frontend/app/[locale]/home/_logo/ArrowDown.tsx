type Props = {
  className?: string
}

export default function ArrowDown ({className}: Props) {
  return (
      <svg className={className} width="62" height="80" viewBox="0 0 62 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g filter="url(#filter0_d_2101_377)">
          <circle cx="26" cy="31" r="31" transform="rotate(-90 31 31)" fill="#111111"/>
          <circle cx="31" cy="31" r="31" transform="rotate(-90 31 31)" fill="#FF584B"/>
          <path d="M31 15 L31 42" stroke="#242233" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M20 35 L31 45 L42 35" stroke="#242233" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round"/>
        </g>
      </svg>
  )
}
