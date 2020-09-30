src = $(wildcard src/*.cpp)
obj = $(src:.cpp=.o)
CC = g++

CXXFLAGS = -g -std=c++11 -lboost_system -lcrypto -lssl -lcpprest

main: $(obj)
	$(CC) -o $@ $^ $(CXXFLAGS)

.PHONY: clean

clean:
	rm -f $(obj) main