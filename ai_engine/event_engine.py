    event_memory[topic] = recent

            count = len(recent)

            if count >= SPIKE_THRESHOLD:

                try:
                    first = min(recent)
                    last = max(recent)
                    duration = max(last - first, 1)
                except:
                    duration = 1

                velocity = count / duration

                spikes.append({
                    "topic": topic,
                    "count": count,
                    "velocity": round(velocity, 4)
                })

        # -------------------------
        # FALLBACK (AYNI MANTIK)
        # -------------------------
        if not spikes and event_memory:

            for topic, times in event_memory.items():
                if times:
                    spikes.append({
                        "topic": topic,
                        "count": len(times),
                        "velocity": 0.0
                    })
                    break

        # -------------------------
        # SORT
        # -------------------------
        try:
            spikes.sort(
                key=lambda x: (x.get("count", 0), x.get("velocity", 0)),
                reverse=True
            )
        except:
            pass

        print("events detected:", len(spikes))

        return spikes

    except:
        return []
