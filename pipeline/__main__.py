

# __main__.py


if __name__ == "__main__":

    try:
        from pipeline.app import NewsPipeline

        pipeline = NewsPipeline()
        pipeline.run()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
