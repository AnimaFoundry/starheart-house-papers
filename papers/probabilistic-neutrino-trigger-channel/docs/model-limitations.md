# Model limitations

This package is an auditable feasibility calculator, not a validated source, detector, network, cost model, or trading strategy.

## Statistical limitations

- Independent binomial trials and Poisson counts omit correlations, burst backgrounds, detector-state changes, clock failures, and adversarial faults.
- A fixed count threshold is not automatically optimal. The sequential likelihood model is valid only when its rate, independence, and timing assumptions hold.
- A false-alarm probability per gate must be multiplied by the number and dependence of null gates; a small per-gate number can still be economically unacceptable.
- Threshold-one detection gives `1-exp(-1)` only when the expected signal count is one under the small-`p`, independent, zero-background model.

## Physical limitations

- `p_eff` is not a magic detector efficiency. It composes spectrum, flavor, oscillation, geometry, cross section, attenuation, target number, acceptance, reconstruction, gating, and dead time.
- No universal inverse-square beam law is asserted. The synthetic divergence model is a sensitivity scenario.
- Spherical chord geometry ignores density variation, topography, source/detector depth, and siting.
- Propagation time is not end-to-end latency. Source command, machine protection, particle production, statistical accumulation, DAQ, classification, authentication, and last-mile routing can dominate.
- Nanosecond timestamps do not imply nanosecond actionable decisions.

## Economic limitations

- No proprietary opportunity sample, exchange feed, broker data, or live trading is used.
- Value, opportunity rate, loss, pulse cost, CAPEX, and alpha decay are synthetic unless explicitly audited.
- Competition, market impact, fees, speed bumps, batch auctions, regulation, and market consolidation can erase private value after physical success.
- Private profit does not establish social value. Energy, infrastructure, fairness, and arms-race externalities are separate tests.

## Relay limitations

- Product-form hop success assumes independence.
- Relay delay includes detection, reconstruction, threshold crossing, decision, safe source command, actuation, production, and pulse formation; it is never represented as FPGA logic alone.
- A relay helps only if a measured flux, detector, attenuation, availability, routing, or cost benefit exceeds reliability and regeneration penalties.

## Evidence limitations

The 2012 experiment is a strong proof of communication in principle but a weak numerical proxy for the proposed use case. Missing integrated source latency, yield per joule, long-baseline beam profile, detector decision latency, authenticated false-trigger rate, infrastructure cost, and market value are not imputed. They remain research targets.
