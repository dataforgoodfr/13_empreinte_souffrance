type Props = {
  href?: string;
  children?: React.ReactNode;
  className? : string;
};

export default function ({ href, children, className }: Props) {
  return (
    <a className={className} href={href}>
      {children}
    </a>
  );
}
