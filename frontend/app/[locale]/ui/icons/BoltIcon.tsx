import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBolt } from '@fortawesome/free-solid-svg-icons';

type BoltIconProps = {
  color?: string;
  fontSize?: string;
};

export default function BoltIcon({ color = '#ff7f7f', fontSize = '40px' }: BoltIconProps) {
  return (
    <span style={{ color: color, fontSize: fontSize }} className={`rotate-[-18deg]`} aria-hidden="true">
      <FontAwesomeIcon icon={faBolt} />
    </span>
  );
}
