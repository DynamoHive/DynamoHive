        signals = [{
                "text": f"system {int(time.time())}",
                "score": 1
            }]

        signals = rank_signals(signals)

        # EVENTS
        for signal in signals:
            register_event(signal.get("text"))

        events = detect_event_spikes()

        # 🔥 BASE INTEL
        raw_intel = synthesize_intelligence(signals, events)

        # 🔥 GERÇEK INTELLIGENCE ENGINE
        try:
            intelligence = intel_engine.process(raw_intel)
        except Exception as e:
            print("INTEL ERROR:", e)
            intelligence = raw_intel

        # CONTENT
        for intel in intelligence:

            topic = intel.get("topic") or f"unknown-{int(time.time())}"

            if is_duplicate(topic):
                logger.info(f"SKIPPED duplicate: {topic}")
                continue

            content = generate_narrative(intel)

            if not content:
                continue

            title = content.get("title") or topic
            body = content.get("content") or "No content"

            save_post(title, body)

            try:
                distribute(content)
            except:
                logger.warning("Distribution failed")

            mark_generated(topic)

            logger.info(f"GENERATED: {topic}")

    except:
        traceback.print_exc()

    finally:
        gc.collect()
        elapsed = round(time.time() - start_time, 2)
        logger.info(f"cycle finished in {elapsed}s")


def start():

    logger.info("DynamoHive system started")

    modules = safe_imports()

    while True:
        try:
            run_cycle(modules)
            time.sleep(CYCLE_INTERVAL)
        except:
            traceback.print_exc()
            time.sleep(ERROR_SLEEP)
