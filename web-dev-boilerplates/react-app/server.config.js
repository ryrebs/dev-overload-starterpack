/** Running pm2's config */
module.exports = [
  {
    script: 'server.js',
    name: 'frontend',
    exec_mode: 'cluster',
    instances: 'max',
  },
];
