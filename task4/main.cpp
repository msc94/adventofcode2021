#include <algorithm>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> split(const std::string &in, const char delim) {
    auto parts = std::vector<std::string>{};
    auto stream = std::stringstream{in};

    auto part = std::string{};
    while (std::getline(stream, part, delim)) {
        if (part == "") {
            continue;
        }

        parts.push_back(part);
    }

    return parts;
}

std::vector<int> transformStringToInt(std::vector<std::string> strings) {
    auto ints = std::vector<int>{};

    std::transform(strings.begin(), strings.end(), std::back_inserter(ints),
                   [](const std::string item) { return std::stoi(item); });

    return ints;
}

std::vector<int> readMarked(std::fstream &stream) {
    auto line = std::string{};
    std::getline(stream, line);

    auto parts = split(line, ',');
    return transformStringToInt(parts);
}

struct Field {
    bool marked[5][5] = {};
    int numbers[5][5] = {};

    void mark(int number) {
        for (size_t i = 0; i < 5; i++) {
            for (size_t j = 0; j < 5; j++) {
                if (numbers[i][j] == number) {
                    marked[i][j] = true;
                    return;
                }
            }
        }
    }

    bool hasWon() {
        for (size_t i = 0; i < 5; i++) {
            auto won = true;

            for (size_t j = 0; j < 5; j++) {
                if (!marked[i][j]) {
                    won = false;
                    break;
                }
            }

            if (won) {
                return true;
            }
        }

        for (size_t j = 0; j < 5; j++) {
            auto won = true;

            for (size_t i = 0; i < 5; i++) {
                if (!marked[i][j]) {
                    won = false;
                    break;
                }
            }

            if (won) {
                return true;
            }
        }

        return false;
    }

    int unmarkedSum() {
        int sum = 0;

        for (size_t i = 0; i < 5; i++) {
            for (size_t j = 0; j < 5; j++) {
                if (!marked[i][j]) {
                    sum += numbers[i][j];
                }
            }
        }

        return sum;
    }
};

std::vector<Field> readFields(std::fstream &stream) {
    auto result = std::vector<Field>{};
    auto line = std::string{};

    while (stream) {
        auto field = Field{};

        // Read empty line
        if (!std::getline(stream, line)) {
            break;
        }

        // Read 5 lines
        for (size_t i = 0; i < 5; i++) {
            std::getline(stream, line);
            auto strings = split(line, ' ');
            auto numbers = transformStringToInt(strings);

            if (numbers.size() != 5) {
                std::cerr << "Wrong size?\n";
                exit(1);
            }

            for (size_t j = 0; j < 5; j++) {
                field.numbers[i][j] = numbers[j];
            }
        }

        result.push_back(field);
    }

    return result;
}

int main(int argc, char **argv) {
    auto fstream = std::fstream("task4/input.txt", std::ios_base::in);
    auto marked = readMarked(fstream);
    auto fields = readFields(fstream);

    for (auto i : marked) {
        for (auto it = fields.begin(); it != fields.end();) {
            it->mark(i);

            if (it->hasWon()) {
                if (fields.size() > 1) {
                    it = fields.erase(it);
                    continue;
                }

                auto unmarked = it->unmarkedSum();
                auto result = unmarked * i;
                std::cout << result << "\n";
                return 0;
            }

            it++;
        }
    }
}