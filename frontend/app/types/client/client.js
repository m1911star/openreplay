import { List } from 'immutable';
import Record from 'Types/Record';
import Site from 'Types/site';
import { DateTime } from 'luxon';
import LoggerOptions from './loggerOptions';

export default Record({
  loggerOptions: LoggerOptions(),
  apiKey: undefined,
  tenantId: undefined,
  name: undefined,
  sites: List(),
  optOut: true
}, {
  fromJS: ({
    projects,
    loggerOptions, 
    ...rest
  }) => ({
    ...rest,
    loggerOptions: LoggerOptions(loggerOptions),
    sites: List(projects).map(Site),
  }),
});
