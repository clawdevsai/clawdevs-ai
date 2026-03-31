import { beforeExecution } from './hooks/before_execution';
import { afterExecution } from './hooks/after_execution';

export { beforeExecution, afterExecution };

export const skillConfig = {
  name: 'dev_backend_implementation',
  version: '2.0.0',
  hooks: {
    beforeExecution,
    afterExecution,
  },
};
