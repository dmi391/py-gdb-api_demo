
include ./paths
#From file 'paths':
#TOOLS
#RISCV_LD_LIBRARY_PATH

#TARGET := Name of current directory:
TARGET := $(notdir $(CURDIR))

SRC_DIR := src
BUILD_DIR := Debug

SRC_CPP := $(wildcard $(SRC_DIR)/*.cpp)
SRC_ASM := $(wildcard $(SRC_DIR)/*.asm)
SRC_S := $(wildcard $(SRC_DIR)/*.S)

OBJECTS := $(addprefix $(BUILD_DIR)/, $(SRC_CPP:.cpp=.o)) \
            $(addprefix $(BUILD_DIR)/, $(SRC_ASM:.asm=.o)) \
            $(addprefix $(BUILD_DIR)/, $(SRC_S:.S=.o))


CXX := $(TOOLS)riscv64-unknown-elf-g++

CXXFLAGS = -march=rv64g -msmall-data-limit=8 -O0 -fmessage-length=0 \
            -fsigned-char -ffunction-sections -fdata-sections -g3 \
            -std=gnu++11 -fabi-version=0 \
            -fno-exceptions -fno-rtti -fno-use-cxa-atexit -fno-threadsafe-statics -fno-unwind-tables \
            -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@)" -c -o "$@" "$<"

LDFLAGS := -march=rv64g -msmall-data-limit=8 -O0 -fmessage-length=0 \
            -fsigned-char -ffunction-sections -fdata-sections -g3 \
            -T"src/link.ld" -nostartfiles \
            -L"${RISCV_LD_LIBRARY_PATH}" \
            -Wl,-Map,"$(BUILD_DIR)/$(TARGET).map" \
            --specs=nosys.specs

LDLIBS := -lc


default:  all 
.PHONY: all
all: link


.PHONY: link
link: $(OBJECTS)
	@echo Linking target: $(TARGET).elf
	@mkdir -p $(dir $@)
	$(CXX) $(LDFLAGS) -o $(BUILD_DIR)/$(TARGET).elf $(OBJECTS) $(LDLIBS)
	@echo ""
	@echo "Post-build:"
	$(TOOLS)riscv64-unknown-elf-objdump -S "$(BUILD_DIR)/$(TARGET).elf" > "$(TARGET).txt"
	$(TOOLS)riscv64-unknown-elf-objcopy -O verilog "$(BUILD_DIR)/$(TARGET).elf" "$(BUILD_DIR)/$(TARGET).hex"
	@echo ""
	@$(TOOLS)riscv64-unknown-elf-size --format=berkeley "$(BUILD_DIR)/$(TARGET).elf"
	@echo ""
	@echo "Done"


#Compile obj-files and generate dependency info
$(BUILD_DIR)/%.o: %.cpp
	@echo Building file: "$@"
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS)
	@echo ""

$(BUILD_DIR)/%.o: %.S
	@echo Building file: "$@"
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS)
	@echo ""

$(BUILD_DIR)/%.o: %.asm
	@echo Building file: "$@"
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS)
	@echo ""

#Include .d files for existing .o files
ifneq ($(strip $(OBJECTS:%.o=%.d)),)
-include $(OBJECTS:%.o=%.d)
endif


.PHONY: clean
clean:
	@echo "Clean..."
	@rm -rf $(BUILD_DIR)/*
