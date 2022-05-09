import React, { Suspense } from "react";

// lazy loaded components via dynamic import from webpack. (Not supported on server side rendered app)
const BarComponent = React.lazy(() => import("./Bar"));

export default () => (
  <div>
    <Suspense fallback={<div>Loading Bar Component...</div>}>
      <p>I am Foo! Pleasure to meet you.</p>
      <BarComponent />
    </Suspense>
  </div>
);
