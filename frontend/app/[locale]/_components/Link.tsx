type Props = {
  href?: string
  children?: React.ReactNode
}

export default function ({href, children}: Props) {
  return (<a className={`bg-gray-100 p-3 text-sm underline border-b-1 border-violet`} href={href}>
    {children}
  </a>)
}
